#!/usr/bin/env python3
"""Download raw data files from the Kenneth R. French Data Library."""
import urllib.request
import zipfile
from pathlib import Path

BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"
FILES = ["Europe_5_Factors_CSV.zip", "Europe_25_Portfolios_ME_BE-ME_CSV.zip"]
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        dest = RAW / f
        print("downloading", f)
        req = urllib.request.Request(BASE + f, headers=UA)
        with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as fh:
            fh.write(r.read())
        with zipfile.ZipFile(dest) as z:
            z.extractall(RAW)
        print("extracted", f)


if __name__ == "__main__":
    main()
