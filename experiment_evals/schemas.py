from dataclasses import dataclass


@dataclass
class AgentStatistics:
    """Statistics reported by the AI analyst for one KPI."""

    control_n: int
    treatment_n: int
    control_mean: float
    treatment_mean: float
    absolute_lift: float
    relative_lift: float
    p_value: float
    ci_lower: float
    ci_upper: float
    significant: bool


@dataclass
class AgentOutput:
    """Complete structured output produced by the AI analyst."""

    analysis: str
    kpis: dict[str, AgentStatistics]


def agent_statistics_from_dict(data: dict) -> AgentStatistics:
    return AgentStatistics(
        control_n=data["control_n"],
        treatment_n=data["treatment_n"],
        control_mean=data["control_mean"],
        treatment_mean=data["treatment_mean"],
        absolute_lift=data["absolute_lift"],
        relative_lift=data["relative_lift"],
        p_value=data["p_value"],
        ci_lower=data["ci_lower"],
        ci_upper=data["ci_upper"],
        significant=data["significant"],
    )


def agent_output_from_dict(data: dict) -> AgentOutput:
    return AgentOutput(
        analysis=data["analysis"],
        kpis={
            kpi_name: agent_statistics_from_dict(kpi_data)
            for kpi_name, kpi_data in data["kpis"].items()
        },
    )
