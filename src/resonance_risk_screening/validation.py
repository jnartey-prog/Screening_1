from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

from resonance_risk_screening.risk_model import derive_risk_thresholds, label_risk_levels


def evaluate_temporal_cv(feature_df: pd.DataFrame, n_splits: int = 4) -> pd.DataFrame:
    """Summarize temporal stability of score thresholds and flag rates."""
    tscv = TimeSeriesSplit(n_splits=n_splits)
    rows: list[dict[str, float | int]] = []
    x = feature_df.reset_index(drop=True)

    for fold, (train_idx, test_idx) in enumerate(tscv.split(x), start=1):
        train_score = x.loc[train_idx, "risk_score"].reset_index(drop=True)
        test_score = x.loc[test_idx, "risk_score"].reset_index(drop=True)
        q1, q2 = derive_risk_thresholds(train_score)
        test_labels = label_risk_levels(test_score, thresholds=(q1, q2))
        rows.append(
            {
                "fold": fold,
                "q1": q1,
                "q2": q2,
                "median_score": float(test_score.median()),
                "high_share": float((test_labels == "high").mean()),
                "moderate_share": float((test_labels == "moderate").mean()),
                "low_share": float((test_labels == "low").mean()),
            }
        )
    return pd.DataFrame(rows)


def _jaccard(a: pd.Series, b: pd.Series) -> float:
    a_bool = a.astype(bool)
    b_bool = b.astype(bool)
    union = int((a_bool | b_bool).sum())
    if union == 0:
        return 1.0
    return float((a_bool & b_bool).sum() / union)


def run_benchmarks(feature_df: pd.DataFrame, labels: pd.Series) -> pd.DataFrame:
    """Compare simple screening heuristics to the reference screening score."""
    reference_high = labels == "high"
    inv_stiff = 1.0 / feature_df["k_stiff"].replace(0.0, np.nan)
    benchmark_scores = {
        "voltage-only": feature_df["v_dep"],
        "loading-only": feature_df["u_inc"],
        "stress-average": pd.concat(
            [
                feature_df["v_dep"],
                feature_df["u_inc"],
                feature_df["c_inc"],
                inv_stiff.fillna(inv_stiff.median()),
            ],
            axis=1,
        ).mean(axis=1),
    }

    rows: list[dict[str, float | str]] = []
    for method, score in benchmark_scores.items():
        method_labels = label_risk_levels(score)
        high_flag = method_labels == "high"
        rows.append(
            {
                "method": method,
                "spearman_rho": float(feature_df["risk_score"].corr(score, method="spearman")),
                "high_risk_overlap": _jaccard(reference_high, high_flag),
                "flagged_share": float(high_flag.mean()),
            }
        )
    return pd.DataFrame(rows)
