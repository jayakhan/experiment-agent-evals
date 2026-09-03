import argparse
import json

import pandas as pd

from experiment_evals.pipeline import evaluate_experiment
from experiment_evals.schemas import agent_output_from_dict


def run_evaluation(
    data_path: str,
    agent_output_path: str,
    expected_control_share: float = 0.5,
):
    """
    Load experiment inputs and run the complete ExperimentEvals pipeline.
    """

    data = pd.read_csv(data_path)

    with open(
        agent_output_path,
        "r",
        encoding="utf-8",
    ) as file:
        raw_agent_output = json.load(file)

    agent_output = agent_output_from_dict(raw_agent_output)

    return evaluate_experiment(
        data=data,
        agent_output=agent_output,
        expected_control_share=expected_control_share,
    )


def aggregate_kpi_metric(
    results: dict,
    layer: str,
    metric_name: str,
):
    """
    Aggregate one KPI-level metric across all KPIs.

    The metric passes only when it passes for every evaluated KPI.
    """

    failed_kpis = []

    for kpi, kpi_results in results["kpis"].items():
        matching_result = next(
            (result for result in kpi_results[layer] if result.metric == metric_name),
            None,
        )

        if matching_result is not None and not matching_result.passed:
            failed_kpis.append(kpi)

    passed = len(failed_kpis) == 0

    return passed, failed_kpis


def print_metric(
    metric_name: str,
    passed: bool,
    failed_kpis: list[str] | None = None,
):
    """
    Print one user-facing ExperimentEvals metric.
    """

    status = "PASS" if passed else "FAIL"

    print(f"{status} | {metric_name}")

    if failed_kpis:
        print("       Affected KPIs: " + ", ".join(failed_kpis))


def print_evaluation(results: dict):
    """
    Print ExperimentEvals results at the evaluation-metric level.
    """

    print("\nExperimentEvals")
    print("=" * 50)

    # --------------------------------------------------
    # ASSUMPTIONS
    # --------------------------------------------------

    print("\nASSUMPTIONS")

    assumption_scores = []

    # Experiment-level SRM
    srm_result = results["experiment_assumptions"][0]

    print_metric(
        metric_name=srm_result.metric,
        passed=srm_result.passed,
    )

    assumption_scores.append(srm_result.passed)

    # KPI-level Missing Data Handling
    missing_passed, missing_failed_kpis = aggregate_kpi_metric(
        results=results,
        layer="assumptions",
        metric_name="Missing Data Handling",
    )

    print_metric(
        metric_name="Missing Data Handling",
        passed=missing_passed,
        failed_kpis=missing_failed_kpis,
    )

    assumption_scores.append(missing_passed)

    # KPI-level Sample Adequacy
    sample_passed, sample_failed_kpis = aggregate_kpi_metric(
        results=results,
        layer="assumptions",
        metric_name="Sample Adequacy",
    )

    print_metric(
        metric_name="Sample Adequacy",
        passed=sample_passed,
        failed_kpis=sample_failed_kpis,
    )

    assumption_scores.append(sample_passed)

    assumptions_passed = sum(assumption_scores)
    assumptions_total = len(assumption_scores)

    print(f"\nAssumptions Score: " f"{assumptions_passed}/{assumptions_total}")

    # --------------------------------------------------
    # STATISTICS
    # --------------------------------------------------

    print("\nSTATISTICS")

    statistic_metrics = [
        "Control Mean",
        "Treatment Mean",
        "Absolute Lift",
        "Relative Lift",
        "P-value",
        "Confidence Interval",
        "Significance",
    ]

    statistic_scores = []

    for metric_name in statistic_metrics:
        passed, failed_kpis = aggregate_kpi_metric(
            results=results,
            layer="statistics",
            metric_name=metric_name,
        )

        print_metric(
            metric_name=metric_name,
            passed=passed,
            failed_kpis=failed_kpis,
        )

        statistic_scores.append(passed)

    statistics_passed = sum(statistic_scores)
    statistics_total = len(statistic_scores)

    print(f"\nStatistics Score: " f"{statistics_passed}/{statistics_total}")

    # --------------------------------------------------
    # OBJECTIVE SUMMARY
    # --------------------------------------------------

    objective_passed = assumptions_passed + statistics_passed
    objective_total = assumptions_total + statistics_total

    print("\n" + "=" * 50)
    print("OBJECTIVE SUMMARY")

    print(f"Assumptions: " f"{assumptions_passed}/{assumptions_total}")

    print(f"Statistics: " f"{statistics_passed}/{statistics_total}")

    print(f"Objective Score: " f"{objective_passed}/{objective_total}")


def parse_args():
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description=("Run ExperimentEvals on an AI-generated " "A/B test analysis.")
    )

    parser.add_argument(
        "--data",
        required=True,
        help="Path to the experiment CSV file.",
    )

    parser.add_argument(
        "--agent-output",
        required=True,
        help="Path to the agent_output.json file.",
    )

    parser.add_argument(
        "--expected-control-share",
        type=float,
        default=0.5,
        help="Expected Control allocation share. Default: 0.5",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    results = run_evaluation(
        data_path=args.data,
        agent_output_path=args.agent_output,
        expected_control_share=args.expected_control_share,
    )

    print_evaluation(results)
