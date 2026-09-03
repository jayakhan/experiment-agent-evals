# ExperimentEvals Instructions

This repository contains ExperimentEvals, a method-aware framework for
evaluating AI-generated A/B test analysis.

## When asked to analyze and evaluate an experiment

Complete the following workflow end to end.

### 1. Analyze

Read the requested experiment dataset.

Use Welch's two-sample t-test for the experiment KPIs.

Provide:
- the required statistical results for each KPI;
- one concise overall interpretation of the experiment across KPIs.

The overall interpretation should:
- summarize the overall pattern of results;
- distinguish upstream and downstream outcomes when relevant;
- mention important conflicting KPI movement;
- contextualize unusually large relative changes using raw counts or
  absolute effects when relevant;
- avoid making recommendations stronger than the evidence supports.

Create `agent_output.json` using the schema in
`experiment_evals/schemas.py`.

The analysis and overall interpretation must be completed before
evaluation begins.

Do not inspect evaluation results before completing the analysis.
Do not revise the analysis after seeing evaluation results.

### 2. Evaluate

Run the existing ExperimentEvals objective evaluation.

Use the repository's evaluation logic for:

- Data Validation, using metrics defined in `experiment_evals/validity_checks.py`.
- Statistics, using metrics defined in `experiment_evals/statistics_checks.py`
- Then evaluate the frozen analyst interpretation using every rubric
defined in `experiment_evals/interpretation_rubrics.py`.
  Currently:
  - Uncertainty / Overclaiming
  - Cross-KPI Synthesis
  - Practical Significance / Effect-Size Interpretation

Do not invent additional evaluation metrics.

### 3. Aggregate at the evaluation-metric level

KPI-level checks are diagnostic evidence only.

Do NOT use KPI × metric checks as the user-facing score denominator.

Each ExperimentEvals metric counts exactly once.

If a metric fails for one or more KPIs, mark that metric FAIL and list
the affected KPIs underneath it.

### 4. Final report

Return the report in this order:

ANALYST INTERPRETATION

Show the original overall experiment interpretation created before
evaluation. Do not rewrite it using evaluation results.

DATA VALIDATION

For each metric:
PASS/FAIL | Metric Name

Then show:
Data Validation Score: X/Y

STATISTICS

For each metric:
PASS/FAIL | Metric Name

Then show:
Statistics Score: X/Y

INTERPRETATION

For each metric:
PASS/FAIL | Metric Name
       Brief evidence-based rationale.

The rationale should explain what in the analyst's original
interpretation caused the PASS or FAIL.

For Practical Significance, explicitly mention raw event counts,
absolute effects, or small baselines when they are important to the
judgment.

Then show:
Interpretation Score: X/Y

ERROR ANALYSIS

Show only failed metrics.

For each failure, include:
- affected KPI(s), when applicable;
- concise reason for failure.

If nothing failed, show:
None.

SUMMARY

Data Validation: X/Y
Statistics: X/Y
Interpretation: X/Y
Overall: X/Y (percentage)

Overall denominator is the number of ExperimentEvals metrics,
not KPI-level checks.

Do not modify ExperimentEvals source code during analysis or evaluation.