from experiment_evals.validity_checks import (
    evaluate_missing_data,
    evaluate_sample_adequacy,
    evaluate_srm,
)
from experiment_evals.statistical_checks import (
    calculate_welch_statistics,
    evaluate_agent_statistics,
)


def evaluate_kpi_analysis(data, kpi: str, reported_statistics):
    """Run KPI-level assumptions and statistical correctness checks."""

    control_values = data.loc[data["Group"] == "Control", kpi]
    treatment_values = data.loc[data["Group"] == "Treatment", kpi]

    assumptions = [
        evaluate_missing_data(
            data=data,
            kpi=kpi,
            reported_control_n=reported_statistics.control_n,
            reported_treatment_n=reported_statistics.treatment_n,
        ),
        evaluate_sample_adequacy(
            control_count=control_values.notna().sum(),
            treatment_count=treatment_values.notna().sum(),
        ),
    ]

    expected_statistics = calculate_welch_statistics(
        control_values=control_values,
        treatment_values=treatment_values,
    )

    statistics = evaluate_agent_statistics(
        expected=expected_statistics,
        reported=reported_statistics,
    )

    return {
        "assumptions": assumptions,
        "statistics": statistics,
    }


def evaluate_experiment(
    data,
    agent_output,
    expected_control_share: float = 0.5,
):
    """Run the deterministic ExperimentEvals pipeline."""

    control_users = data.loc[data["Group"] == "Control", "Visitor ID"].nunique()
    treatment_users = data.loc[data["Group"] == "Treatment", "Visitor ID"].nunique()

    experiment_assumptions = [
        evaluate_srm(
            control_users=control_users,
            treatment_users=treatment_users,
            expected_control_share=expected_control_share,
        )
    ]

    kpis = {
        kpi: evaluate_kpi_analysis(data, kpi, reported_statistics)
        for kpi, reported_statistics in agent_output.kpis.items()
    }

    return {
        "analysis": agent_output.analysis,
        "experiment_assumptions": experiment_assumptions,
        "kpis": kpis,
    }
