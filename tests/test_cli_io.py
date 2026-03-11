from __future__ import annotations

from pathlib import Path

import pytest

from resonance_risk_screening import io


@pytest.mark.unit
def test_load_operational_data_missing_columns_raises(tmp_path: Path):
    p = tmp_path / "bad.csv"
    p.write_text("timestamp,v_bus\n2024-01-01,11.0\n", encoding="utf-8")
    with pytest.raises(ValueError):
        io.load_operational_data(p)
