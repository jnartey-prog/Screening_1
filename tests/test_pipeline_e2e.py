from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from resonance_risk_screening.pipeline import ResonancePipeline


@pytest.mark.e2e
def test_pipeline_run_generates_outputs(tmp_path: Path, synthetic_df: pd.DataFrame):
    input_path = tmp_path / "input.csv"
    out_dir = tmp_path / "artifacts"
    synthetic_df.to_csv(input_path, index=False)

    pipeline = ResonancePipeline()
    outputs = pipeline.run(input_path, out_dir)

    assert outputs["predictions"].exists()
    assert outputs["cv_metrics"].exists()
    assert outputs["benchmarks"].exists()
    assert outputs["table_1"].exists()
    assert outputs["figure_1"].exists()
    assert outputs["artifact_manifest"].exists()
    assert (tmp_path / "logs" / "run.log").exists()
    assert (tmp_path / "logs" / "run.jsonl").exists()
