#!/usr/bin/env python3
from __future__ import annotations

import argparse

from gisgpt.validator import validate_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a VFM manifest.")
    parser.add_argument("manifest")
    args = parser.parse_args()

    report = validate_manifest(args.manifest)
    for warning in report.warnings:
        print(f"WARNING: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}")
    print("OK" if report.ok else "FAILED")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
