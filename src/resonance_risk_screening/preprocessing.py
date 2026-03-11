from __future__ import annotations

import numpy as np
import pandas as pd


def _mad_mask(series: pd.Series, threshold: float = 6.0) -> pd.Series:
    median = float(series.median())
    abs_dev = (series - median).abs()
    mad = float(abs_dev.median())
    if mad == 0.0:
        return pd.Series([False] * len(series), index=series.index)
    modified_z = 0.6745 * (series - median).abs() / mad
    return modified_z > threshold


def preprocess_operational_data(df: pd.DataFrame) -> pd.DataFrame:
    """Align timestamps, interpolate missing values, and filter extreme outliers."""
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], errors="coerce")
    out = out.dropna(subset=["timestamp"]).sort_values("timestamp")
    out = out.drop_duplicates(subset=["timestamp"]).set_index("timestamp")

    numeric_cols = [c for c in out.columns if pd.api.types.is_numeric_dtype(out[c])]
    out[numeric_cols] = out[numeric_cols].interpolate(method="linear", limit_direction="both")

    for col in numeric_cols:
        mask = _mad_mask(out[col])
        if mask.any():
            out.loc[mask, col] = np.nan
    out[numeric_cols] = out[numeric_cols].interpolate(method="linear", limit_direction="both")

    # Simple per-unit normalization defaults if ratings are not supplied.
    if "i_inc_rated" not in out.columns:
        out["i_inc_rated"] = max(float(out["i_inc"].max()), 1.0)
    if "v_nom" not in out.columns:
        out["v_nom"] = max(float(out["v_bus"].median()), 1.0)

    out = out.reset_index()
    return out
