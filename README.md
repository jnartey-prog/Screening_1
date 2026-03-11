# Resonance Risk Screening

[![CI](https://img.shields.io/badge/CI-configured-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
[![PyPI](https://img.shields.io/badge/PyPI-planned-blue)](#)

Python package for physics-guided reduced-order screening of harmonic resonance susceptibility in 33/11 kV substations.

## Quick Start

```bash
uv run resonance-pipeline --input data.csv --output-dir manuscript/artifacts
```

## Core Workflow

1. Load and preprocess operational data.
2. Compute physics-guided proxies.
3. Reconstruct operating states.
4. Estimate resonance-risk score and class probabilities.
5. Generate manuscript tables and figures.

## Documentation

Full docs are in `docs/` and can be built with Sphinx.
