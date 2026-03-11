"""Public package API for resonance risk screening.

Examples:
    >>> import resonance_risk_screening as rrs
    >>> isinstance(rrs.__version__, str)
    True
"""

__version__ = "0.1.0"

from resonance_risk_screening.artifacts import generate_manuscript_artifacts
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
from resonance_risk_screening.user_api import ScreeningSession, read, screen
from resonance_risk_screening.validation import evaluate_temporal_cv, run_benchmarks

__all__ = [
    "ResonancePipeline",
    "load_operational_data",
    "preprocess_operational_data",
    "compute_proxies",
    "cluster_operating_states",
    "compute_resonance_score",
    "label_risk_levels",
    "train_ordinal_model",
    "evaluate_temporal_cv",
    "run_benchmarks",
    "generate_manuscript_artifacts",
    "read",
    "screen",
    "ScreeningSession",
    "__version__",
]
