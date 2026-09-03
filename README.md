# ExperimentEvals

ExperimentEvals is a method-aware evaluation framework for AI-generated A/B test analysis. Deterministic checks independently recompute results in Python, while interpretation quality is evaluated using rubric-based LLM judgment.

It evaluates:

- **Experiment data validity** — deterministic evaluation  
  Sample Ratio Mismatch, Missing Data Handling, Sample Adequacy

- **Statistical correctness** — deterministic evaluation  
  Control Mean, Treatment Mean, Absolute Lift, Relative Lift, P-value, Confidence Interval, Significance

- **Interpretation quality** — LLM-as-a-judge  
  Uncertainty / Overclaiming, Cross-KPI Synthesis, Practical Significance / Effect-Size Interpretation

## Prerequisites

- Python 3.10+
- VS Code
- GitHub Copilot
- Git

Create a virtual environment and install dependencies.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Quick Start

1. Clone the repository and open it in VS Code.
2. Activate the virtual environment.
3. Open GitHub Copilot Chat and run:

> Follow .github/copilot-instructions.md. Analyze your_experiment.csv as an A/B test using Welch’s two-sample t-test and evaluate the analysis using ExperimentEvals.

To try the framework first, use the sample experiment included in this repository:

> Follow .github/copilot-instructions.md. Analyze sample_experiment.csv as an A/B test using Welch’s two-sample t-test and evaluate the analysis using ExperimentEvals.

Copilot analyzes the experiment, creates the structured output required by ExperimentEvals, runs the evaluation framework, and returns the final evaluation.

## Example Output

```text
EXPERIMENT ANALYSIS INTERPRETATION
<overall experiment interpretation>

VALIDITY
PASS | Sample Ratio Mismatch
PASS | Missing Data Handling
PASS | Sample Adequacy
Score: 3/3

STATISTICS
PASS | Control Mean
PASS | Treatment Mean
PASS | Absolute Lift
PASS | Relative Lift
PASS | P-value
PASS | Confidence Interval
PASS | Significance
Score: 7/7

INTERPRETATION
PASS | Uncertainty / Overclaiming
PASS | Cross-KPI Synthesis
PASS | Practical Significance / Effect-Size Interpretation
Score: 3/3

OVERALL
13/13
```

## Project Structure

```text
experiment-evals/
├── .github/
│   └── copilot-instructions.md      # defines the analyze → freeze → evaluate workflow for Copilot
├── experiment_evals/
│   ├── __init__.py                  # marks experiment_evals as a Python package
│   ├── validity_checks.py           # SRM, missing-data handling, and sample-adequacy checks
│   ├── statistical_checks.py        # Welch statistics and statistical metric evaluation
│   ├── interpretation_rubrics.py    # uncertainty, synthesis, and practical-significance rubrics
│   ├── schemas.py                   # structured agent_output.json schema
│   ├── pipeline.py                  # coordinates evaluation across the experiment and KPIs
│   └── runner.py                    # runs objective checks and aggregates metric-level results
├── sample_experiment.csv            # sample dataset for getting started
├── README.md                        # project overview and usage instructions
├── requirements.txt                 # Python dependencies
└── .gitignore                       # files excluded from version control
```

## Current Scope

ExperimentEvals currently supports two-group A/B tests analyzed with Welch’s two-sample t-test.

The Sample Adequacy threshold is a configurable prototype guardrail and should not be interpreted as a universal statistical rule.

## Design Principle

When a result can be independently recomputed, ExperimentEvals uses deterministic evaluation. LLM-based rubric evaluation is reserved for semantic judgments that cannot be reliably reduced to a deterministic calculation.

## Future Enhancements

Potential extensions include:

- additional experiment designs and statistical methods;
- configurable experiment-quality guardrails;
- independent LLM judges for interpretation evaluation;
- component level and trace-level evaluation;
- broader experimentation-specific failure-mode libraries.

## References

- Andrew Ng, DeepLearning.AI — *Agentic AI*
- DeepLearning.AI / Arize AI — *Evaluating AI Agents*
- Anthropic — *Demystifying Evals for AI Agents*
- Liu et al. (2024) — *AgentBench: Evaluating LLMs as Agents*, ICLR 2024
