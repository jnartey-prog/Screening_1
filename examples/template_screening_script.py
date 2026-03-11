"""Template script for non-coder users.

EDIT HERE:
1) Set INPUT_CSV to your dataset path.
2) Set OUTPUT_DIR to where you want results.
3) Run: uv run python examples/template_screening_script.py
"""

from pathlib import Path

import resonance_risk_screening as rrs

INPUT_CSV = Path("data/substation_scada_33_11kv.csv")
OUTPUT_DIR = Path("manuscript/artifacts")


def main() -> None:
    # One-liner default workflow
    outputs = rrs.screen(INPUT_CSV, OUTPUT_DIR)
    print("Screening complete.")
    for key, value in outputs.items():
        print(f"{key}: {value}")

    # Optional method-chaining workflow
    session = rrs.ScreeningSession().load(INPUT_CSV).prep().fit()
    print(session.summary())


if __name__ == "__main__":
    main()
