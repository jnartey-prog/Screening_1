from __future__ import annotations

import pytest

from resonance_risk_screening.preprocessing import preprocess_operational_data
from resonance_risk_screening.proxies import compute_proxies


@pytest.mark.unit
def test_compute_proxies_columns(synthetic_df):
    clean = preprocess_operational_data(synthetic_df)
    proxy = compute_proxies(clean)
    expected = {
        "timestamp",
        "v_dep",
        "v_imb",
        "u_inc",
        "c_inc",
        "load_ramp",
        "ramp_dispersion",
        "k_stiff",
    }
    assert expected.issubset(set(proxy.columns))
    assert len(proxy) == len(clean)
