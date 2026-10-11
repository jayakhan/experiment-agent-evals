from dataclasses import dataclass
from math import isclose

import numpy as np
from scipy.stats import t, ttest_ind

from experiment_evals.schemas import AgentStatistics


@dataclass
class StatisticResult:
    metric: str
    passed: bool
    description: str


def calculate_welch_statistics(
    control_values,
    treatment_values,
    alpha: float = 0.05,
):
    """Independently calculate Welch two-sample statistics."""

    control = np.asarray(control_values, dtype=float)
    treatment = np.asarray(treatment_values, dtype=float)
    control = control[~np.isnan(control)]
    treatment = treatment[~np.isnan(treatment)]

    control_mean = np.mean(control)
    treatment_mean = np.mean(treatment)
    absolute_lift = treatment_mean - control_mean
    relative_lift = absolute_lift / control_mean

    test_result = ttest_ind(treatment, control, equal_var=False)
    p_value = test_result.pvalue

    control_var = np.var(control, ddof=1)
    treatment_var = np.var(treatment, ddof=1)
    control_n = len(control)
    treatment_n = len(treatment)

    standard_error = np.sqrt(
        (control_var / control_n) + (treatment_var / treatment_n)
    )

    numerator = (
        (control_var / control_n) + (treatment_var / treatment_n)
    ) ** 2
    denominator = (
        ((control_var / control_n) ** 2) / (control_n - 1)
        + ((treatment_var / treatment_n) ** 2) / (treatment_n - 1)
    )
    degrees_of_freedom = numerator / denominator

    critical_value = t.ppf(1 - alpha / 2, degrees_of_freedom)
    margin_of_error = critical_value * standard_error

    return {
        "control_mean": control_mean,
        "treatment_mean": treatment_mean,
        "absolute_lift": absolute_lift,
        "relative_lift": relative_lift,
        "p_value": p_value,
        "confidence_interval": (
            absolute_lift - margin_of_error,
            absolute_lift + margin_of_error,
        ),
        "significant": p_value < alpha,
    }


def evaluate_agent_statistics(
    expected: dict,
    reported: AgentStatistics,
) -> list[StatisticResult]:
    """Compare AI-reported statistics with independent calculations."""

    checks = [
        ("Control Mean", isclose(reported.control_mean, expected["control_mean"], rel_tol=0.01, abs_tol=0.0001)),
        ("Treatment Mean", isclose(reported.treatment_mean, expected["treatment_mean"], rel_tol=0.01, abs_tol=0.0001)),
        ("Absolute Lift", isclose(reported.absolute_lift, expected["absolute_lift"], rel_tol=0.01, abs_tol=0.0001)),
        ("Relative Lift", isclose(reported.relative_lift, expected["relative_lift"], rel_tol=0.01, abs_tol=0.0001)),
        ("P-value", isclose(reported.p_value, expected["p_value"], rel_tol=0.05, abs_tol=0.001)),
        (
            "Confidence Interval",
            isclose(reported.ci_lower, expected["confidence_interval"][0], rel_tol=0.01, abs_tol=0.001)
            and isclose(reported.ci_upper, expected["confidence_interval"][1], rel_tol=0.01, abs_tol=0.001),
        ),
        ("Significance", reported.significant == expected["significant"]),
    ]

    return [
        StatisticResult(
            metric=metric,
            passed=passed,
            description=(
                f"{metric} check passed."
                if passed
                else f"{metric} check failed."
            ),
        )
        for metric, passed in checks
    ]
