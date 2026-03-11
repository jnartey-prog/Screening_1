from pathlib import Path

from resonance_risk_screening.pipeline import ResonancePipeline


def main() -> None:
    pipeline = ResonancePipeline()
    outputs = pipeline.run(Path("data/substation_scada_33_11kv.csv"), Path("manuscript/artifacts"))
    for key, value in outputs.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
