from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from pydantic import ValidationError

from .vfm_schema import VFMManifest, load_manifest


@dataclass
class ValidationReport:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def validate_manifest(path: str | Path) -> ValidationReport:
    try:
        manifest = load_manifest(path)
    except (OSError, ValueError, ValidationError) as exc:
        return ValidationReport(ok=False, errors=[str(exc)])

    warnings: list[str] = []

    if not manifest.provenance:
        warnings.append("missing provenance")
    if not manifest.assets:
        warnings.append("manifest has no modality assets")
    if not manifest.entities:
        warnings.append("manifest has no entities")
    if manifest.split not in {None, "train", "validation", "test"}:
        warnings.append(f"non-standard split label: {manifest.split}")
    if not any(
        [
            manifest.split_key.spatial_cell,
            manifest.split_key.temporal_bucket,
            manifest.split_key.scene_id,
            manifest.split_key.source_group,
        ]
    ):
        warnings.append("missing leakage-control split keys")

    return ValidationReport(ok=True, warnings=warnings)


def leakage_conflicts(manifests: Iterable[VFMManifest]) -> list[str]:
    """Detect group overlap across train/validation/test.

    Random row-level splits are unsafe for spatial datasets because neighboring
    tiles, repeated scenes or adjacent time steps can leak nearly identical
    information into evaluation.
    """
    groups: dict[tuple[str, str], set[str]] = {}
    for m in manifests:
        if not m.split:
            continue
        for kind, value in (
            ("spatial_cell", m.split_key.spatial_cell),
            ("temporal_bucket", m.split_key.temporal_bucket),
            ("scene_id", m.split_key.scene_id),
            ("source_group", m.split_key.source_group),
        ):
            if value:
                groups.setdefault((kind, value), set()).add(m.split)

    conflicts = []
    for (kind, value), splits in groups.items():
        if len(splits) > 1:
            conflicts.append(f"{kind}={value!r} appears in splits {sorted(splits)}")
    return conflicts
