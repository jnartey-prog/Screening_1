from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_operational_data(path: Path) -> pd.DataFrame:
    """Load CSV operational data with required basic schema checks."""
    df = pd.read_csv(path)
    required = {"timestamp", "v_bus", "i_inc", "p_total"}
    missing = sorted(required - set(df.columns))
    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(
            f"Missing required columns: {missing_str}. "
            "Expected at least: timestamp, v_bus, i_inc, p_total."
        )
    return df
