from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel

from resonance_risk_screening.interfaces import BaseModelAdapter

RiskClass = Literal["low", "moderate", "high"]


def compute_resonance_score(proxy_df: pd.DataFrame) -> pd.Series:
    """Compute reduced-order resonance susceptibility score."""
    denom = proxy_df["k_stiff"].replace(0.0, np.nan)
    score = (proxy_df["v_dep"] * proxy_df["u_inc"] * proxy_df["c_inc"]) / denom
    return score.fillna(0.0).clip(lower=0.0)


def label_risk_levels(score: pd.Series) -> pd.Series:
    """Label low/moderate/high risk via quantile thresholds."""
    q1 = float(score.quantile(0.33))
    q2 = float(score.quantile(0.66))

    def _label(v: float) -> str:
        if v <= q1:
            return "low"
        if v <= q2:
            return "moderate"
        return "high"

    return score.apply(_label)


@dataclass
class OrdinalRiskModel(BaseModelAdapter):
    model: OrderedModel
    result: Any
    feature_columns: list[str]

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        probs = self.result.model.predict(self.result.params, exog=X[self.feature_columns])
        return pd.DataFrame(probs, columns=["low", "moderate", "high"], index=X.index)

    def metadata(self) -> dict[str, Any]:
        return {"model": "ordered_logit", "features": self.feature_columns}


def train_ordinal_model(feature_df: pd.DataFrame, labels: pd.Series) -> OrdinalRiskModel:
    """Train cumulative logit model for ordered risk classes."""
    feature_columns = ["v_dep", "u_inc", "c_inc", "k_stiff", "load_ramp", "ramp_dispersion"]
    y = labels.map({"low": 0, "moderate": 1, "high": 2})
    model = OrderedModel(y, feature_df[feature_columns], distr="logit")
    result = model.fit(method="bfgs", disp=False)
    return OrdinalRiskModel(model=model, result=result, feature_columns=feature_columns)
