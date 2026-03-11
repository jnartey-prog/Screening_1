from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import pandas as pd


class BasePipeline(ABC):
    """Abstract pipeline interface for fluent workflow implementations."""

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> "BasePipeline":
        raise NotImplementedError

    @abstractmethod
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def run(self, input_path: Path, output_dir: Path) -> dict[str, Path]:
        raise NotImplementedError


class BaseModelAdapter(ABC):
    """Adapter interface for model wrappers returning probabilities."""

    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def metadata(self) -> dict[str, Any]:
        raise NotImplementedError
