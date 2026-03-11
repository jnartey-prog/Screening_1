from __future__ import annotations

from pathlib import Path

import pandas as pd

from resonance_risk_screening.pipeline import ResonancePipeline


def main() -> None:
    input_path = Path("data/substation_scada_33_11kv.csv")
    output_dir = Path("manuscript/artifacts")
    if not input_path.exists():
        raise FileNotFoundError(
            "Expected input dataset at data/substation_scada_33_11kv.csv for artifact generation."
        )
    pipeline = ResonancePipeline()
    outputs = pipeline.run(input_path, output_dir)
    pd.Series({k: str(v) for k, v in outputs.items()}).to_csv(
        output_dir / "artifact_manifest.csv", header=["path"]
    )


if __name__ == "__main__":
    main()
