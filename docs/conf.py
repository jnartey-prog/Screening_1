import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

project = "resonance-risk-screening"
author = "Research Team"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build"]
html_theme = "alabaster"
