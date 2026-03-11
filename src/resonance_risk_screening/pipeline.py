from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from resonance_risk_screening.artifacts import generate_manuscript_artifacts
from resonance_risk_screening.clustering import cluster_operating_states
from resonance_risk_screening.interfaces import BasePipeline
from resonance_risk_screening.io import load_operational_data
from resonance_risk_screening.logging_config import build_logger
from resonance_risk_screening.preprocessing import preprocess_operational_data
from resonance_risk_screening.proxies import compute_proxies
from resonance_risk_screening.risk_model import (
    compute_resonance_score,
    label_risk_levels,
    train_ordinal_model,
)
from resonance_risk_screening.validation import evaluate_temporal_cv, run_benchmarks


class ResonancePipeline(BasePipeline):
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path
        self.model: Any | None = None

    def fit(self, df: pd.DataFrame) -> "ResonancePipeline":
        clean = preprocess_operational_data(df)
        proxy_df = compute_proxies(clean)
        proxy_df["risk_score"] = compute_resonance_score(proxy_df)
        labels = label_risk_levels(proxy_df["risk_score"])
        self.model = train_ordinal_model(proxy_df, labels)
        return self

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.model is None:
            raise RuntimeError("Model not fitted. Call fit() before predict().")
        clean = preprocess_operational_data(df)
        proxy_df = compute_proxies(clean)
        proxy_df["risk_score"] = compute_resonance_score(proxy_df)
        labels = label_risk_levels(proxy_df["risk_score"])
        probs = self.model.predict_proba(proxy_df)
        out = proxy_df.copy()
        out["risk_label"] = labels.values
        out = pd.concat([out, probs], axis=1)
        return out

    def run(self, input_path: Path, output_dir: Path) -> dict[str, Path]:
        log_dir = output_dir / ".." / "logs"
        logger = build_logger(log_dir.resolve())
        logger.info("Pipeline started", extra={"extra_payload": {"stage": "start", "status": "ok"}})

        raw_df = load_operational_data(input_path)
        clean_df = preprocess_operational_data(raw_df)
        proxy_df = compute_proxies(clean_df)
        clustered = cluster_operating_states(proxy_df, n_clusters=3)
        clustered["risk_score"] = compute_resonance_score(clustered)
        labels = label_risk_levels(clustered["risk_score"])
        model = train_ordinal_model(clustered, labels)
        probs = model.predict_proba(clustered)

        results_df = clustered.copy()
        results_df["risk_label"] = labels.values
        results_df = pd.concat([results_df, probs], axis=1)

        cv_metrics = evaluate_temporal_cv(results_df, labels)
        benchmark_metrics = run_benchmarks(results_df, labels)

        output_dir.mkdir(parents=True, exist_ok=True)
        pred_path = output_dir / "risk_predictions.csv"
        cv_path = output_dir / "cv_metrics.csv"
        bench_path = output_dir / "benchmark_metrics.csv"

        results_df.to_csv(pred_path, index=False)
        cv_metrics.to_csv(cv_path, index=False)
        benchmark_metrics.to_csv(bench_path, index=False)

        manifest = generate_manuscript_artifacts(
            {"proxy_df": results_df, "cv_metrics": cv_metrics, "benchmarks": benchmark_metrics},
            output_dir,
        )
        manifest_path = output_dir.parent / "artifact_manifest.yaml"
        manifest_payload = {k: str(v) for k, v in manifest.items()}
        manifest_payload.update(
            {
                "predictions": str(pred_path),
                "cv_metrics": str(cv_path),
                "benchmarks": str(bench_path),
            }
        )
        manifest_path.write_text(yaml.safe_dump(manifest_payload, sort_keys=True), encoding="utf-8")

        logger.info(
            "Pipeline finished",
            extra={
                "extra_payload": {
                    "stage": "complete",
                    "status": "ok",
                    "output_dir": str(output_dir),
                }
            },
        )
        return {
            "predictions": pred_path,
            "cv_metrics": cv_path,
            "benchmarks": bench_path,
            "table_1": manifest["table_1"],
            "figure_1": manifest["figure_1"],
            "artifact_manifest": manifest_path,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run resonance risk screening pipeline.")
    parser.add_argument("--input", type=Path, required=True, help="Path to input CSV.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for outputs.")
    args = parser.parse_args()

    pipeline = ResonancePipeline()
    pipeline.run(args.input, args.output_dir)
