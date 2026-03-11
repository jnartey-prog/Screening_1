from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from resonance_risk_screening.clustering import cluster_operating_states
from resonance_risk_screening.io import load_operational_data
from resonance_risk_screening.pipeline import ResonancePipeline
from resonance_risk_screening.preprocessing import preprocess_operational_data
from resonance_risk_screening.proxies import compute_proxies
from resonance_risk_screening.risk_model import (
    compute_resonance_score,
    label_risk_levels,
    train_ordinal_model,
)


def read(path: str | Path) -> pd.DataFrame:
    """Load operational data from CSV path."""
    return load_operational_data(Path(path))


def screen(path: str | Path, output_dir: str | Path = "manuscript/artifacts") -> dict[str, Path]:
    """One-liner screening workflow with defaults."""
    return ResonancePipeline().run(Path(path), Path(output_dir))


@dataclass
class ScreeningSession:
    """Fluent, method-chaining workflow for non-coder-friendly analysis."""

    raw_df: pd.DataFrame | None = None
    data: pd.DataFrame | None = None
    proxies: pd.DataFrame | None = None
    result: pd.DataFrame | None = None
    model: Any | None = None
    notes: list[str] = field(default_factory=list)

    def load(self, path: str | Path) -> "ScreeningSession":
        self.raw_df = read(path)
        self.notes.append(f"Loaded {len(self.raw_df)} rows.")
        return self

    def prep(self) -> "ScreeningSession":
        if self.raw_df is None:
            raise ValueError("No data loaded. Call load(path) first.")
        self.data = preprocess_operational_data(self.raw_df)
        self.notes.append("Preprocessing completed.")
        return self

    def fit(self) -> "ScreeningSession":
        if self.data is None:
            raise ValueError("No preprocessed data available. Call prep() first.")
        self.proxies = compute_proxies(self.data)
        clustered = cluster_operating_states(self.proxies)
        clustered["risk_score"] = compute_resonance_score(clustered)
        clustered["risk_label"] = label_risk_levels(clustered["risk_score"])
        self.model = train_ordinal_model(clustered, clustered["risk_label"])
        probs = self.model.predict_proba(clustered)
        self.result = pd.concat([clustered, probs], axis=1)
        self.notes.append("Model fitting and scoring completed.")
        return self

    def summary(self) -> pd.DataFrame:
        if self.result is None:
            raise ValueError("No results yet. Call fit() first.")
        return (
            self.result["risk_label"]
            .value_counts(dropna=False)
            .rename_axis("risk_label")
            .reset_index(name="count")
        )

    def plot(self) -> plt.Figure:
        if self.result is None:
            raise ValueError("No results yet. Call fit() first.")
        fig, ax = plt.subplots(figsize=(7, 4))
        self.result["risk_score"].plot(ax=ax)
        ax.set_title("Resonance Risk Score Trend")
        ax.set_xlabel("Sample index")
        ax.set_ylabel("Risk score")
        ax.grid(alpha=0.3)
        fig.tight_layout()
        return fig
