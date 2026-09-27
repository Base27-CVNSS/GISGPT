#!/usr/bin/env python3
"""Minimal canonicalization entry point.

This intentionally starts from manifests rather than pretending that one parser
can correctly normalize every GIS/BIM/robotics format. Production adapters
should be modality-specific and must preserve provenance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gisgpt.vfm_schema import VFMManifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", help="JSON object matching the VFM draft schema")
    parser.add_argument("output_vfm")
    args = parser.parse_args()

    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    manifest = VFMManifest.model_validate(payload)
    Path(args.output_vfm).write_text(
        manifest.model_dump_json(indent=2, exclude_none=True),
        encoding="utf-8",
    )
    print(f"Canonical VFM manifest written to {args.output_vfm}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
