from __future__ import annotations

import argparse
from pathlib import Path

from resonance_risk_screening.pipeline import ResonancePipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive resonance screening CLI.")
    parser.add_argument("--input", type=Path, help="Input CSV path.")
    parser.add_argument("--output-dir", type=Path, help="Output directory path.")
    args = parser.parse_args()

    input_path = args.input
    if input_path is None:
        input_path = Path(input("Enter input CSV path: ").strip())

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = Path(input("Enter output directory: ").strip())

    pipeline = ResonancePipeline()
    outputs = pipeline.run(input_path, output_dir)
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(title="Pipeline Outputs")
        table.add_column("Artifact")
        table.add_column("Path")
        for key, value in outputs.items():
            table.add_row(str(key), str(value))
        console.print(table)
    except Exception:
        print("Pipeline complete.")
        for k, v in outputs.items():
            print(f"{k}: {v}")
