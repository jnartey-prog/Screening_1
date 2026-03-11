from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def synthetic_df() -> pd.DataFrame:
    n = 120
    t = pd.date_range("2024-01-01", periods=n, freq="h")
    rng = np.random.default_rng(42)
    base = np.linspace(0, 8, n)
    return pd.DataFrame(
        {
            "timestamp": t,
            "v_bus": 11.0 - 0.03 * np.sin(base),
            "i_inc": 150 + 20 * np.sin(base) + rng.normal(0, 2, n),
            "p_total": 2.0 + 0.5 * np.sin(base) + rng.normal(0, 0.02, n),
            "i_f_1": 70 + 10 * np.sin(base + 0.2),
            "i_f_2": 50 + 7 * np.sin(base + 0.5),
            "i_f_3": 30 + 5 * np.sin(base + 0.9),
        }
    )
