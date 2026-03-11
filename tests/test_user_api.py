from __future__ import annotations

from pathlib import Path

import pytest

import resonance_risk_screening as rrs


@pytest.mark.unit
def test_top_level_read(synthetic_df, tmp_path: Path):
    p = tmp_path / "in.csv"
    synthetic_df.to_csv(p, index=False)
    df = rrs.read(p)
    assert len(df) == len(synthetic_df)


@pytest.mark.integration
def test_method_chaining_session(synthetic_df, tmp_path: Path):
    p = tmp_path / "in.csv"
    synthetic_df.to_csv(p, index=False)
    session = rrs.ScreeningSession().load(p).prep().fit()
    summary = session.summary()
    assert not summary.empty
    fig = session.plot()
    assert fig is not None


@pytest.mark.e2e
def test_one_liner_screen(synthetic_df, tmp_path: Path):
    p = tmp_path / "in.csv"
    out_dir = tmp_path / "art"
    synthetic_df.to_csv(p, index=False)
    outputs = rrs.screen(p, out_dir)
    assert outputs["predictions"].exists()
