#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from gisgpt.tasks import build_instruction_examples
from gisgpt.vfm_schema import load_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate spatial SFT JSONL from a VFM manifest.")
    parser.add_argument("manifest")
    parser.add_argument("output")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    rows = build_instruction_examples(manifest)
    out = Path(args.output)
    out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} examples to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
