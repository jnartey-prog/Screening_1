from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd

from resonance_risk_screening.interfaces import BaseModelAdapter

RiskClass = Literal["low", "moderate", "high"]


def _robust_standardize(series: pd.Series) -> pd.Series:
    median = float(series.median())
    iqr = float(series.quantile(0.75) - series.quantile(0.25))
    scale = iqr if iqr > 0 else max(float(series.std(ddof=0)), 1.0)
    return (series - median) / scale


def compute_resonance_score(proxy_df: pd.DataFrame) -> pd.Series:
    """Compute a transparent reduced-order screening score from proxy indicators."""
    inv_stiff = 1.0 / proxy_df["k_stiff"].replace(0.0, np.nan)
    components = pd.DataFrame(
        {
            "v_dep": _robust_standardize(proxy_df["v_dep"]),
            "v_imb": _robust_standardize(proxy_df["v_imb"]),
            "u_inc": _robust_standardize(proxy_df["u_inc"]),
            "c_inc": _robust_standardize(proxy_df["c_inc"]),
            "load_ramp": _robust_standardize(proxy_df["load_ramp"].abs()),
            "ramp_dispersion": _robust_standardize(proxy_df["ramp_dispersion"]),
            "inv_k_stiff": _robust_standardize(inv_stiff.fillna(inv_stiff.median())),
        }
    ).fillna(0.0)

    weights = pd.Series(
        {
            "v_dep": 0.30,
            "v_imb": 0.05,
            "u_inc": 0.20,
            "c_inc": 0.10,
            "load_ramp": 0.10,
            "ramp_dispersion": 0.10,
            "inv_k_stiff": 0.15,
        }
    )
    score = components.mul(weights, axis=1).sum(axis=1)
    score = score - float(score.min())
    return score.clip(lower=0.0)


def derive_risk_thresholds(score: pd.Series) -> tuple[float, float]:
    q1 = float(score.quantile(0.33))
    q2 = float(score.quantile(0.66))
    return q1, q2


def label_risk_levels(score: pd.Series, thresholds: tuple[float, float] | None = None) -> pd.Series:
    """Label low/moderate/high risk via predeclared score thresholds."""
    q1, q2 = thresholds if thresholds is not None else derive_risk_thresholds(score)

    def _label(v: float) -> str:
        if v <= q1:
            return "low"
        if v <= q2:
            return "moderate"
        return "high"

    return score.apply(_label)


@dataclass
class HeuristicRiskModel(BaseModelAdapter):
    thresholds: tuple[float, float]
    scale: float

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        score = X["risk_score"] if "risk_score" in X.columns else compute_resonance_score(X)
        q1, q2 = self.thresholds
        scale = max(self.scale, 1e-6)
        low_arg = np.clip((score - q1) / scale, -60.0, 60.0)
        high_arg = np.clip((q2 - score) / scale, -60.0, 60.0)
        low = 1.0 / (1.0 + np.exp(low_arg))
        high = 1.0 / (1.0 + np.exp(high_arg))
        moderate = np.clip(1.0 - low - high, 1e-6, None)
        probs = pd.DataFrame({"low": low, "moderate": moderate, "high": high}, index=X.index)
        probs = probs.div(probs.sum(axis=1), axis=0)
        return probs

    def metadata(self) -> dict[str, Any]:
        q1, q2 = self.thresholds
        return {"model": "heuristic_score_calibration", "q1": q1, "q2": q2, "scale": self.scale}


def train_ordinal_model(feature_df: pd.DataFrame, labels: pd.Series | None = None) -> HeuristicRiskModel:
    """Return a score-calibration model for screening probabilities.

    The retained function name preserves the public API, but the returned object
    is a transparent calibration wrapper rather than a supervised classifier.
    """

    score = feature_df["risk_score"] if "risk_score" in feature_df.columns else compute_resonance_score(feature_df)
    thresholds = derive_risk_thresholds(score)
    scale = float((score.quantile(0.75) - score.quantile(0.25)) / 4.0)
    if scale <= 0:
        scale = max(float(score.std(ddof=0)) / 4.0, 1e-3)
    return HeuristicRiskModel(thresholds=thresholds, scale=scale)
