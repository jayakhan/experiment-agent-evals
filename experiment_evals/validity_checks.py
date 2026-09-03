from dataclasses import dataclass

from scipy.stats import chisquare


@dataclass
class AssumptionResult:
    metric: str
    passed: bool
    description: str


def evaluate_srm(
    control_users: int,
    treatment_users: int,
    expected_control_share: float = 0.5,
    alpha: float = 0.05,
) -> AssumptionResult:
    """Check observed visitor allocation against the planned split."""

    total_users = control_users + treatment_users
    expected_counts = [
        total_users * expected_control_share,
        total_users * (1 - expected_control_share),
    ]
    observed_counts = [control_users, treatment_users]

    _, p_value = chisquare(f_obs=observed_counts, f_exp=expected_counts)
    passed = p_value >= alpha

    return AssumptionResult(
        metric="Sample Ratio Mismatch",
        passed=passed,
        description=(
            "Sample Ratio Mismatch check passed."
            if passed
            else "Sample Ratio Mismatch check failed."
        ),
    )


def evaluate_missing_data(
    data,
    kpi: str,
    reported_control_n: int,
    reported_treatment_n: int,
    group_column: str = "Group",
) -> AssumptionResult:
    """Check whether the AI used the correct non-missing sample sizes."""

    actual_control_n = data.loc[data[group_column] == "Control", kpi].notna().sum()
    actual_treatment_n = data.loc[data[group_column] == "Treatment", kpi].notna().sum()

    passed = (
        reported_control_n == actual_control_n
        and reported_treatment_n == actual_treatment_n
    )

    return AssumptionResult(
        metric="Missing Data Handling",
        passed=passed,
        description=(
            "Missing Data Handling check passed."
            if passed
            else "Missing Data Handling check failed."
        ),
    )


def evaluate_sample_adequacy(
    control_count: int,
    treatment_count: int,
    minimum_count: int = 10,
) -> AssumptionResult:
    """Apply the current MVP minimum-sample rule to both groups."""

    passed = control_count >= minimum_count and treatment_count >= minimum_count

    return AssumptionResult(
        metric="Sample Adequacy",
        passed=passed,
        description=(
            "Sample Adequacy check passed."
            if passed
            else "Sample Adequacy check failed."
        ),
    )
