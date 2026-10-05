"""Data loaders: French Data Library files and generic CSVs."""
from __future__ import annotations

import re
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

FRENCH_BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
FRENCH_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

#: Sentinel used by the French library for missing values.
MISSING = -99.99


def download_french_file(filename: str, dest_dir: str | Path) -> Path:
    """Download one ``*_CSV.zip`` from the French Data Library and extract it."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename
    req = urllib.request.Request(FRENCH_BASE + filename, headers=FRENCH_UA)
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as fh:
        fh.write(r.read())
    with zipfile.ZipFile(dest) as z:
        z.extractall(dest_dir)
    # the extracted CSV usually shares the zip's stem, e.g. Europe_5_Factors.csv
    stem = filename.removesuffix(".zip").removesuffix("_CSV") + ".csv"
    extracted = dest_dir / stem
    return extracted if extracted.exists() else dest


class FrenchLibraryLoader:
    """Download + parse Kenneth R. French Data Library files."""

    def __init__(self, raw_dir: str | Path):
        self.raw_dir = Path(raw_dir)

    def download(self, *filenames: str) -> list[Path]:
        return [download_french_file(f, self.raw_dir) for f in filenames]

    def load_factors(self, path: str | Path) -> pd.DataFrame:
        return load_french_factors(path)

    def load_portfolios(self, path: str | Path) -> pd.DataFrame:
        return load_french_portfolios(path)


def load_french_factors(path: str | Path) -> pd.DataFrame:
    """Parse the monthly block of a French-library factor file.

    Returns a DataFrame indexed by month-end date, values in percent
    (the library's convention), e.g. columns ``Mkt-RF, SMB, HML, RMW, CMA, RF``.
    """
    lines = Path(path).read_text().splitlines()
    # header row looks like ",Mkt-RF,SMB,HML,RMW,CMA,RF"
    start = next(i for i, l in enumerate(lines) if l.startswith(",Mkt-RF"))
    cols = [c.strip() for c in lines[start].split(",")[1:]]
    return _parse_monthly_block(lines[start + 1:], cols)


def load_french_portfolios(path: str | Path) -> pd.DataFrame:
    """Parse the value-weighted monthly block of a 25-portfolio file."""
    lines = Path(path).read_text().splitlines()
    start = next(
        i for i, l in enumerate(lines)
        if l.strip() == "Average Value Weighted Returns -- Monthly"
    )
    cols = [c.strip() for c in lines[start + 1].split(",")[1:]]
    return _parse_monthly_block(lines[start + 2:], cols)


def _parse_monthly_block(lines: list[str], cols: list[str]) -> pd.DataFrame:
    rows = []
    for line in lines:
        if not line.strip():
            break
        parts = line.split(",")
        date = parts[0].strip()
        if not re.fullmatch(r"\d{6}", date):
            break
        vals = [float(p) for p in parts[1:1 + len(cols)]]
        rows.append([date] + vals)
    df = pd.DataFrame(rows, columns=["date"] + cols)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m")
    return df.set_index("date").replace(MISSING, np.nan)


def load_csv(path: str | Path, date_col: str = "date") -> pd.DataFrame:
    """Load a generic CSV of monthly series (user-supplied data)."""
    df = pd.read_csv(path, parse_dates=[date_col])
    return df.set_index(date_col).sort_index()
