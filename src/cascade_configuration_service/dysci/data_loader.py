from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "policy",
    "edge_model",
    "cloud_model",
    "threshold",
    "cost",
    "error",
    "estimated_latency_ms",
}

NUMERIC_COLUMNS = [
    "threshold",
    "cost",
    "error",
    "estimated_latency_ms",
]


def load_policy_table(file_path: Path) -> pd.DataFrame:
    """Load and validate the offline-generated DYSCI policy table."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Policy table not found: {file_path.resolve()}"
        )

    table = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS - set(table.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    for column in NUMERIC_COLUMNS:
        table[column] = pd.to_numeric(table[column], errors="coerce")

    return table.dropna(subset=NUMERIC_COLUMNS)
