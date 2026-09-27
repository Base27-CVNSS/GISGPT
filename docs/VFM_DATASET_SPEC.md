# VFM Training Dataset Profile 0.1 — Draft

> This document defines a **training-data profile layered on top of VFM**. It is not a replacement for a byte-level VFM binary/core specification. The purpose is to make heterogeneous spatial data auditable, alignable and learnable by AI systems.

## 1. Design objective

Traditional GIS files usually optimize one representation at a time: vector, raster, point cloud, tiles, BIM or time series. Foundation-model training requires something different: a stable way to bind **objects, geometry, time, semantics, sensor state, relations and provenance** without forcing every modality into the same physical encoding.

The VFM training profile therefore separates:

1. **canonical identity and metadata**;
2. **modality assets/chunks**;
3. **spatial-temporal relationships**;
4. **indexes**;
5. **training/evaluation split controls**;
6. **provenance and governance**.

## 2. Canonical object model

A VFM sample should expose the following logical layers.

| Layer | Required role |
|---|---|
| Identity | Stable dataset/sample/entity identifiers |
| Reference frame | CRS, axis order, units, vertical datum, local/world frames |
| Geometry | Vector, 3D boxes, mesh references, footprints, extents |
| Observation | Raster, image/video, LiDAR, point cloud, sensor streams |
| Time | Valid time, acquisition time, state sequence, trajectory |
| Topology | contains, intersects, touches, connected_to, upstream_of, etc. |
| Semantics | Class labels, ontologies, text descriptions, external dictionaries |
| Provenance | Source, license, acquisition time, transformations, hashes |
| Index | Spatial, temporal, entity and semantic lookup structures |
| Split key | Geographic/time/scene/source grouping for leakage-safe evaluation |

## 3. Modality contract

### 3.1 Vector
Store geometry in a canonical spatial reference or provide an explicit transform. Preserve stable feature IDs and schema provenance.

### 3.2 Raster / imagery
Record pixel-to-world transform, CRS, resolution, bands, nodata, acquisition time and radiometric provenance.

### 3.3 Point cloud / LiDAR
Record frame, scale/offset, coordinate system, timestamp, sensor pose/calibration, semantic labels and links to corresponding entities where available.

### 3.4 BIM / IFC
Preserve IFC GlobalId when lawful and stable. Map BIM objects to world coordinates using explicit transforms. Keep object class, containment hierarchy and relationships separate from render meshes.

### 3.5 Trajectory / SLAM
Represent ordered poses with timestamps and frame relationships. A trajectory is not just a polyline; pose, orientation, covariance and sensor frame matter.

### 3.6 Sensor / IoT
Bind observations to feature-of-interest, observed property, time and units. OGC SensorThings concepts are a useful interoperability target.

### 3.7 Mesh / 3D scene
Keep geometry, material/rendering assets and semantic object identity separable. 3D Tiles, glTF and OpenUSD-style scene representations may be referenced as assets rather than duplicated.

## 4. Coordinate and frame discipline

Every spatial sample must answer:

- What is the horizontal CRS?
- What is the vertical reference?
- What are the units?
- What is the axis order?
- Is geometry in a global, map, vehicle, camera, BIM-local or sensor frame?
- What transform connects local frames to the world frame?
- What is the timestamp of that transform?

Training records lacking this information should be rejected or downgraded rather than silently normalized.

## 5. Topology and relation vocabulary

Relations should be explicit triples:

```text
(subject_id, predicate, object_id)
```

Suggested relation families:

- qualitative direction: north_of, left_of, above, below;
- metric/proximity: within_distance, nearest_to;
- topology: intersects, touches, contains, within, overlaps, disjoint;
- network: connected_to, upstream_of, reachable_from;
- BIM: hosted_by, part_of, adjacent_space;
- temporal: before, after, co_occurs, changes_to;
- robotics: visible_from, traversable_from, obstructs, supports.

Derived relations must store their derivation/evidence so the training corpus can distinguish observations from computed labels.

## 6. Semantic layer

Semantics should not be hard-wired into geometry bytes. The profile supports external controlled vocabularies or dictionaries so the same geometric entity can be interpreted in multiple domains/languages.

This enables a practical split:

```text
VFM core = identity + geometry + values + topology + indexes
semantic dictionary = terminology / ontology / multilingual descriptions
runtime = joins the two when needed
```

## 7. Provenance

Each asset or sample should record, where applicable:

- source URL/system;
- data owner/provider;
- acquisition/retrieval time;
- license;
- transformation chain;
- software/version;
- checksum/content hash;
- annotation method;
- human/AI validation status.

A training example without provenance may still be usable experimentally, but it must not be indistinguishable from audited ground truth.

## 8. Leakage-safe split policy

Random feature-level splitting is prohibited for benchmark claims when neighboring tiles, repeated captures, the same building, the same road corridor or adjacent timestamps can appear across splits.

At least one grouping key should be held out by:

- geography;
- time;
- physical scene/object;
- data source;
- sensor campaign.

Strong evaluation uses multiple simultaneous holdouts.

## 9. Training views

The same VFM sample can generate different learnable views:

1. **Text view** — descriptions, metadata, documentation.
2. **Graph view** — entities + topology/relations.
3. **Tool view** — validated GIS/BIM operations and parameters.
4. **Raster view** — image/remote-sensing tokens.
5. **3D view** — point-cloud/mesh/BIM embeddings.
6. **Temporal view** — trajectories and state sequences.
7. **World-model view** — current state → future/next state prediction.

These views share stable IDs so cross-modal alignment does not rely on filename heuristics.

## 10. Failure behavior

A compliant data pipeline should fail loudly for:

- unknown CRS/units when metric labels are required;
- invalid geometry that changes the target relation;
- broken entity references;
- missing frame transforms for multimodal alignment;
- duplicate stable IDs;
- split leakage;
- missing license information for restricted publication/training;
- hash mismatch.

## 11. Interoperability targets

VFM should bridge to, not replace, mature standards:

- OGC/ISO geospatial standards for CRS and spatial models;
- CityGML for semantic 3D city models;
- OGC SensorThings for observations/tasking;
- buildingSMART IFC for BIM;
- 3D Tiles/glTF for streaming/rendering;
- common point-cloud formats such as LAS/LAZ;
- GeoParquet/COG/PMTiles as efficient distribution/analytics encodings.

VFM's research role is the **cross-modal identity, relation, time and provenance layer** used to build consistent AI training samples.
