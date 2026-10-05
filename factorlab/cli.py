"""Command-line interface: ``python -m factorlab run <config.yaml>``."""
from __future__ import annotations

import argparse
from pathlib import Path


def main(argv: list[str] | None = None) -> None:
    from factorlab.data.loaders import FrenchLibraryLoader
    from factorlab.pipeline import run

    ap = argparse.ArgumentParser(prog="factorlab",
                                 description="YAML-configured factor research")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="run a study from a YAML config")
    p_run.add_argument("config", help="path to config.yaml")

    p_dl = sub.add_parser("download", help="download French-library files")
    p_dl.add_argument("files", nargs="+", help="e.g. Europe_5_Factors_CSV.zip")
    p_dl.add_argument("--dest", default="data/raw",
                      help="destination directory (default: data/raw)")

    args = ap.parse_args(argv)
    if args.cmd == "run":
        run(args.config)
    elif args.cmd == "download":
        loader = FrenchLibraryLoader(args.dest)
        for p in loader.download(*args.files):
            print("ready:", p)


if __name__ == "__main__":
    main()
