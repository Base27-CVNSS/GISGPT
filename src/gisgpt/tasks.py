from __future__ import annotations

from typing import Any

from .vfm_schema import VFMManifest


def relation_instruction_examples(manifest: VFMManifest) -> list[dict[str, Any]]:
    """Create auditable relation-learning examples from explicit VFM triples."""
    entity_by_id = {e.id: e for e in manifest.entities}
    rows: list[dict[str, Any]] = []

    for rel in manifest.relations:
        subject = entity_by_id[rel.subject]
        obj = entity_by_id[rel.object]
        rows.append(
            {
                "task": "spatial_relation",
                "sample_id": manifest.sample_id,
                "instruction": (
                    f"Given VFM entities {subject.id} ({subject.type}) and "
                    f"{obj.id} ({obj.type}), determine their recorded spatial relation."
                ),
                "input": {
                    "subject_bbox": subject.bbox,
                    "object_bbox": obj.bbox,
                    "crs": manifest.crs.model_dump(),
                },
                "output": {
                    "subject": rel.subject,
                    "predicate": rel.predicate,
                    "object": rel.object,
                },
                "provenance_required": True,
            }
        )
    return rows


def tool_plan_examples(manifest: VFMManifest) -> list[dict[str, Any]]:
    """Generate deterministic-tool planning examples without teaching the LLM
    to pretend it is the geometry engine.
    """
    rows: list[dict[str, Any]] = []
    projected = manifest.crs.authority.upper() == "EPSG" and manifest.crs.code not in {"4326", "4979"}

    rows.append(
        {
            "task": "tool_plan",
            "sample_id": manifest.sample_id,
            "instruction": "Plan a metric buffer operation around selected vector entities.",
            "input": {"crs": manifest.crs.model_dump(), "distance_m": 500},
            "output": {
                "preconditions": [
                    "validate geometry",
                    "use a suitable projected CRS in metres" if not projected else "confirm CRS units are metres",
                ],
                "tool_family": "deterministic_gis",
                "operation": "buffer",
                "postconditions": ["validate output geometry", "record CRS and parameters"],
            },
        }
    )
    return rows


def build_instruction_examples(manifest: VFMManifest) -> list[dict[str, Any]]:
    return relation_instruction_examples(manifest) + tool_plan_examples(manifest)
