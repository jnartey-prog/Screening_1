from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import TimeSeriesSplit

from resonance_risk_screening.risk_model import label_risk_levels


def _macro_f1(y_true: pd.Series, y_pred: pd.Series) -> float:
    return float(f1_score(y_true, y_pred, average="macro"))


def evaluate_temporal_cv(
    feature_df: pd.DataFrame, labels: pd.Series, n_splits: int = 4
) -> pd.DataFrame:
    """Compute leakage-safe temporal CV metrics with simple label baseline."""
    tscv = TimeSeriesSplit(n_splits=n_splits)
    rows: list[dict[str, float | int]] = []
    y = labels.reset_index(drop=True)
    x = feature_df.reset_index(drop=True)

    for fold, (train_idx, test_idx) in enumerate(tscv.split(x), start=1):
        train_score = (x.loc[train_idx, "v_dep"] * x.loc[train_idx, "u_inc"]).fillna(0.0)
        test_score = (x.loc[test_idx, "v_dep"] * x.loc[test_idx, "u_inc"]).fillna(0.0)
        q1 = float(train_score.quantile(0.33))
        q2 = float(train_score.quantile(0.66))
        pred = pd.Series(
            np.where(test_score <= q1, "low", np.where(test_score <= q2, "moderate", "high")),
            index=test_idx,
        )
        truth = y.loc[test_idx]
        rows.append(
            {
                "fold": fold,
                "accuracy": float(accuracy_score(truth, pred)),
                "macro_f1": _macro_f1(truth, pred),
            }
        )
    return pd.DataFrame(rows)


def run_benchmarks(feature_df: pd.DataFrame, labels: pd.Series) -> pd.DataFrame:
    """Run simple benchmark screening methods."""
    y_true = labels
    score_a = feature_df["v_dep"]
    pred_a = label_risk_levels(score_a)

    score_b = feature_df["u_inc"]
    pred_b = label_risk_levels(score_b)

    score_c = feature_df[["v_dep", "u_inc", "c_inc", "k_stiff"]].mean(axis=1)
    pred_c = label_risk_levels(score_c)

    return pd.DataFrame(
        [
            {
                "method": "voltage-threshold",
                "accuracy": float(accuracy_score(y_true, pred_a)),
                "macro_f1": _macro_f1(y_true, pred_a),
            },
            {
                "method": "load-threshold",
                "accuracy": float(accuracy_score(y_true, pred_b)),
                "macro_f1": _macro_f1(y_true, pred_b),
            },
            {
                "method": "unweighted-proxy",
                "accuracy": float(accuracy_score(y_true, pred_c)),
                "macro_f1": _macro_f1(y_true, pred_c),
            },
        ]
    )
