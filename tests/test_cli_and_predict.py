from __future__ import annotations

from pathlib import Path

import pytest

from resonance_risk_screening.cli import main as cli_main
from resonance_risk_screening.pipeline import ResonancePipeline


@pytest.mark.integration
def test_pipeline_fit_predict_contains_probabilities(synthetic_df):
    p = ResonancePipeline()
    p.fit(synthetic_df)
    pred = p.predict(synthetic_df)
    assert {"low", "moderate", "high", "risk_label"}.issubset(set(pred.columns))


@pytest.mark.e2e
def test_cli_runs_with_arguments(tmp_path: Path, synthetic_df, monkeypatch):
    in_csv = tmp_path / "in.csv"
    out_dir = tmp_path / "out"
    synthetic_df.to_csv(in_csv, index=False)
    monkeypatch.setattr(
        "sys.argv",
        ["resonance-screen", "--input", str(in_csv), "--output-dir", str(out_dir)],
    )
    cli_main()
    assert (out_dir / "risk_predictions.csv").exists()
