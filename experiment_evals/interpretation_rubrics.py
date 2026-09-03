"""Rubrics used by Copilot for the semantic interpretation layer."""

UNCERTAINTY_RUBRIC = """
Metric: Uncertainty / Overclaiming

PASS if the analysis communicates the strength and limitations of the evidence
without making claims stronger than the experiment supports.

FAIL if the analysis presents inconclusive evidence as a confirmed effect,
claims unjustified certainty, or recommends action as though uncertain evidence
were established.
""".strip()


CROSS_KPI_RUBRIC = """
Metric: Cross-KPI Synthesis

PASS if the analysis considers the overall pattern across relevant KPIs and
acknowledges important conflicting or mixed results.

FAIL if the analysis cherry-picks a favorable KPI, ignores important
contradictory evidence, or gives an overall conclusion inconsistent with the
broader KPI pattern.
""".strip()

PRACTICAL_SIGNIFICANCE_RUBRIC = """
Evaluate whether the experiment analysis interprets effect size in a
practically meaningful way.

PASS if:
- the analysis distinguishes absolute effects from relative effects
  when that distinction matters;
- large relative lifts from very small baselines are contextualized;
- very small raw event counts are acknowledged when they materially
  affect how a result should be interpreted;
- the analysis considers the actual magnitude of the observed effect;
- the analysis avoids recommending action based only on a large-looking
  percentage change.

FAIL if:
- the analysis treats a large relative lift as automatically meaningful;
- it ignores very small raw event counts when they are important;
- it ignores that an absolute effect is small while emphasizing a large
  relative percentage;
- it overstates results driven by a tiny baseline;
- it recommends action based primarily on a large-looking relative change.

Return:
- PASS or FAIL
- one brief evidence-based rationale explaining the judgment.
"""
