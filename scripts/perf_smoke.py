from __future__ import annotations

import time
from pathlib import Path

from resonance_risk_screening.pipeline import ResonancePipeline


def main() -> None:
    input_path = Path("data/substation_scada_33_11kv.csv")
    output_dir = Path("manuscript/artifacts")
    if not input_path.exists():
        print("No fixture data found; skipping perf smoke.")
        return

    start = time.perf_counter()
    ResonancePipeline().run(input_path, output_dir)
    elapsed = time.perf_counter() - start
    if elapsed > 30.0:
        raise RuntimeError(
            f"Performance smoke failed: runtime {elapsed:.2f}s exceeds 30s threshold."
        )
    print(f"Performance smoke passed in {elapsed:.2f}s.")


if __name__ == "__main__":
    main()
