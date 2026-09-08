import pandas as pd


def select_best_policy(
    policy_table: pd.DataFrame,
    cost_budget: float,
    error_budget: float,
) -> tuple[pd.Series | None, pd.DataFrame]:
    """Select the lowest-latency feasible configuration."""

    feasible = policy_table[
        (policy_table["cost"] <= cost_budget)
        & (policy_table["error"] <= error_budget)
    ].copy()

    if feasible.empty:
        return None, feasible

    feasible = feasible.sort_values(
        by=["estimated_latency_ms", "error", "cost"],
        ascending=[True, True, True],
    )

    return feasible.iloc[0], feasible
