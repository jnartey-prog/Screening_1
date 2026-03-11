from __future__ import annotations

import pytest

from resonance_risk_screening.preprocessing import preprocess_operational_data
from resonance_risk_screening.proxies import compute_proxies
from resonance_risk_screening.risk_model import (
    compute_resonance_score,
    label_risk_levels,
    train_ordinal_model,
)


@pytest.mark.unit
def test_train_ordinal_model_and_predict(synthetic_df):
    clean = preprocess_operational_data(synthetic_df)
    proxy = compute_proxies(clean)
    proxy["risk_score"] = compute_resonance_score(proxy)
    labels = label_risk_levels(proxy["risk_score"])
    model = train_ordinal_model(proxy, labels)
    probs = model.predict_proba(proxy)
    assert {"low", "moderate", "high"}.issubset(set(probs.columns))
    assert len(probs) == len(proxy)
