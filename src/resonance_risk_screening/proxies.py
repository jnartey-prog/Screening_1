from __future__ import annotations

import numpy as np
import pandas as pd


def _feeder_current_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("i_f_")]


def compute_proxies(df: pd.DataFrame) -> pd.DataFrame:
    """Compute physics-guided operational proxy indicators."""
    out = df.copy()
    feeder_cols = _feeder_current_columns(out)
    if not feeder_cols:
        # Fallback to one synthetic feeder from incomer if feeder channels are missing.
        out["i_f_1"] = out["i_inc"].values
        feeder_cols = ["i_f_1"]

    v_nom = out.get("v_nom", pd.Series(np.maximum(out["v_bus"].median(), 1.0), index=out.index))
    out["v_dep"] = (v_nom - out["v_bus"]) / v_nom

    if {"v_a", "v_b", "v_c"}.issubset(set(out.columns)):
        vmax = out[["v_a", "v_b", "v_c"]].max(axis=1)
        vmin = out[["v_a", "v_b", "v_c"]].min(axis=1)
        vavg = out[["v_a", "v_b", "v_c"]].mean(axis=1).replace(0.0, np.nan)
        out["v_imb"] = (vmax - vmin) / vavg
    else:
        out["v_imb"] = 0.0

    i_inc_rated = out.get(
        "i_inc_rated", pd.Series(np.maximum(out["i_inc"].max(), 1.0), index=out.index)
    )
    out["u_inc"] = out["i_inc"] / i_inc_rated.replace(0.0, np.nan)

    for c in feeder_cols:
        rated_col = f"{c}_rated"
        if rated_col not in out.columns:
            out[rated_col] = max(float(out[c].max()), 1.0)
        out[f"u_{c}"] = out[c] / out[rated_col].replace(0.0, np.nan)

    feeder_sum = out[feeder_cols].sum(axis=1).replace(0.0, np.nan)
    shares = out[feeder_cols].div(feeder_sum, axis=0).fillna(0.0)
    out["c_inc"] = (shares**2).sum(axis=1)

    out["load_ramp"] = out["p_total"].diff().fillna(0.0)
    feeder_ramps = out[feeder_cols].diff().fillna(0.0)
    out["ramp_dispersion"] = feeder_ramps.std(axis=1).fillna(0.0)

    dp = out["p_total"].diff().fillna(0.0)
    dv = out["v_bus"].diff().replace(0.0, np.nan)
    out["k_stiff"] = (dp / dv).abs().replace([np.inf, -np.inf], np.nan).bfill().fillna(1.0)
    out["k_stiff"] = out["k_stiff"].clip(lower=1e-6)

    cols = [
        "v_dep",
        "v_imb",
        "u_inc",
        "c_inc",
        "load_ramp",
        "ramp_dispersion",
        "k_stiff",
    ]
    return out[["timestamp", *cols]].copy()
