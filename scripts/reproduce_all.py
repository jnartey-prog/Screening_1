from __future__ import annotations

from pathlib import Path
import runpy


def main() -> None:
    runpy.run_path("manuscript/generation_script.py", run_name="__main__")
    required = [
        Path("manuscript/artifacts/risk_predictions.csv"),
        Path("manuscript/artifacts/table_1_symbols.csv"),
        Path("manuscript/artifacts/figure_1_framework.png"),
        Path("manuscript/artifact_manifest.yaml"),
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise RuntimeError(f"Reproducibility replay failed, missing: {missing}")
    print("Reproducibility replay passed.")


if __name__ == "__main__":
    main()
