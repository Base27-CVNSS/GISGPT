from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator


class Modality(str, Enum):
    VECTOR = "vector"
    RASTER = "raster"
    POINT_CLOUD = "point_cloud"
    MESH = "mesh"
    BIM = "bim"
    IMAGE = "image"
    VIDEO = "video"
    TRAJECTORY = "trajectory"
    SENSOR = "sensor"
    TEXT = "text"


class SpatialReference(BaseModel):
    authority: str = "EPSG"
    code: str
    axis_order: str = "xy"
    vertical_datum: str | None = None


class TimeExtent(BaseModel):
    start: str | None = None
    end: str | None = None


class Provenance(BaseModel):
    source: str
    license: str | None = None
    retrieved_at: str | None = None
    transform_history: list[str] = Field(default_factory=list)
    checksum: str | None = None


class AssetRef(BaseModel):
    id: str
    modality: Modality
    uri: str
    media_type: str | None = None
    checksum: str | None = None
    timestamp: str | None = None
    frame_id: str | None = None
    transform_to_world: list[float] | None = None


class Entity(BaseModel):
    id: str
    type: str
    geometry_ref: str | None = None
    bbox: list[float] | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    semantic_labels: list[str] = Field(default_factory=list)
    valid_time: TimeExtent | None = None

    @model_validator(mode="after")
    def validate_bbox(self) -> "Entity":
        if self.bbox is not None:
            if len(self.bbox) not in (4, 6):
                raise ValueError("bbox must be [xmin,ymin,xmax,ymax] or 3D [xmin,ymin,zmin,xmax,ymax,zmax]")
            if len(self.bbox) == 4 and not (self.bbox[0] <= self.bbox[2] and self.bbox[1] <= self.bbox[3]):
                raise ValueError("invalid 2D bbox ordering")
            if len(self.bbox) == 6 and not (
                self.bbox[0] <= self.bbox[3]
                and self.bbox[1] <= self.bbox[4]
                and self.bbox[2] <= self.bbox[5]
            ):
                raise ValueError("invalid 3D bbox ordering")
        return self


class Relation(BaseModel):
    subject: str
    predicate: str
    object: str
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)


class IndexSpec(BaseModel):
    spatial: str | None = None
    temporal: str | None = None
    entity: str | None = None
    semantic: str | None = None


class SplitKey(BaseModel):
    spatial_cell: str | None = None
    temporal_bucket: str | None = None
    scene_id: str | None = None
    source_group: str | None = None


class VFMManifest(BaseModel):
    vfm_version: str = "0.1-draft"
    dataset_id: str
    sample_id: str
    crs: SpatialReference
    bbox: list[float] | None = None
    time_extent: TimeExtent | None = None
    assets: list[AssetRef] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)
    indexes: IndexSpec = Field(default_factory=IndexSpec)
    split: str | None = None
    split_key: SplitKey = Field(default_factory=SplitKey)
    provenance: list[Provenance] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_integrity(self) -> "VFMManifest":
        entity_ids = [x.id for x in self.entities]
        asset_ids = [x.id for x in self.assets]

        if len(entity_ids) != len(set(entity_ids)):
            raise ValueError("entity IDs must be unique")
        if len(asset_ids) != len(set(asset_ids)):
            raise ValueError("asset IDs must be unique")

        known = set(entity_ids)
        for rel in self.relations:
            if rel.subject not in known:
                raise ValueError(f"relation subject not found: {rel.subject}")
            if rel.object not in known:
                raise ValueError(f"relation object not found: {rel.object}")

        known_assets = set(asset_ids)
        for ent in self.entities:
            if ent.geometry_ref and ent.geometry_ref not in known_assets:
                raise ValueError(f"entity geometry_ref not found: {ent.geometry_ref}")

        return self


def load_manifest(path: str | Path) -> VFMManifest:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return VFMManifest.model_validate(payload)


def dump_manifest(manifest: VFMManifest, path: str | Path) -> None:
    Path(path).write_text(
        manifest.model_dump_json(indent=2, exclude_none=True),
        encoding="utf-8",
    )
