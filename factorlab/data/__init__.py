"""Data loaders for factorlab.

Supported inputs:
  - Kenneth R. French Data Library CSVs (fixed-format, monthly blocks)
  - Generic CSVs with a date column (user-supplied factors / test assets)
"""
from factorlab.data.loaders import (
    FrenchLibraryLoader,
    download_french_file,
    load_csv,
    load_french_factors,
    load_french_portfolios,
)

__all__ = [
    "FrenchLibraryLoader",
    "download_french_file",
    "load_csv",
    "load_french_factors",
    "load_french_portfolios",
]
