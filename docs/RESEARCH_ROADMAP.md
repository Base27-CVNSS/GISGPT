# Research Roadmap — VFM-SpatialLM

## Phase 0 — Do not start with model training

The first scientific contribution should be **dataset discipline**.

Build converters and validators for a small number of modalities first:

```text
GeoJSON/GeoParquet
COG/raster
LAS/LAZ point cloud
IFC
trajectory/pose JSON
SensorThings-like observations
        ↓
VFM canonical manifests
```

Success criterion: the same physical object can be linked across at least two modalities with explicit CRS/frame/time/provenance.

## Phase 1 — Text + structure baseline

Reproduce a BB-GeoGPT-like baseline using a modern open model and clean-room data.

Compare:

- Base LLM;
- geographic DAPT only;
- geographic DAPT + SFT;
- VFM text serialization;
- VFM text + relation graph serialization.

This isolates whether VFM structure adds value before introducing expensive multimodal encoders.

## Phase 2 — Tool-grounded GIS

Train the model to produce typed operations rather than free-form Python first.

Example target:

```json
{
  "operation": "buffer",
  "inputs": ["hospital_layer"],
  "parameters": {"distance": 500, "unit": "m"},
  "preconditions": ["project_to_metric_crs"],
  "validator": ["geometry_validity", "crs_units"]
}
```

Execution belongs to GDAL/PROJ/GEOS/PostGIS/GeoPandas/OSMnx or equivalent deterministic backends.

Primary metrics:

- valid tool-call rate;
- correct operation;
- correct parameters;
- CRS/unit error rate;
- executable workflow success;
- postcondition validation success.

## Phase 3 — Multimodal VFM

Add modality encoders one at a time.

### Raster / remote sensing
Use a geospatial visual encoder and learn a projector into the language-model token space.

### Point cloud / LiDAR
Use a point-cloud encoder. Preserve coordinate frame and 3D object grounding rather than reducing the cloud to a caption.

### BIM
Encode IFC object hierarchy, property graph and geometry references. Compare graph serialization against learned graph encoders.

### Trajectory / SLAM
Encode pose sequences with timestamp, orientation and uncertainty. Evaluate relative-pose and navigation tasks.

### Sensor / IoT
Encode multivariate temporal observations tied to spatial entities.

## Phase 4 — World-model extension

A language model alone is not a physical world model. Introduce an explicit state representation:

```text
State_t = {
  objects,
  geometry,
  topology,
  pose,
  sensor state,
  environment,
  time
}
```

Then study:

```text
(State_t, Action_t) → predicted State_(t+1)
```

The model may combine:

- multimodal encoders;
- spatial memory;
- dynamics/latent state model;
- LLM planner;
- deterministic physics/GIS constraints.

Evaluate prediction separately from language quality.

## Phase 5 — Digital Twin bridge

Build adapters:

```text
GIS ↔ VFM ↔ BIM/IFC
           ↕
       IoT/Sensors
           ↕
   Digital Twin State
           ↕
 Drone / UGV / robot / vehicle
```

The central research question is whether a shared VFM object identity and spatiotemporal relation layer improves cross-domain transfer.

## Phase 6 — Robust benchmark

Create **VFM-Bench** with geographically and temporally disjoint test sets.

Task groups:

1. spatial language;
2. geometry/topology;
3. CRS and coordinate reasoning;
4. GIS tool use;
5. map/visual reasoning;
6. point-cloud/3D grounding;
7. BIM relationship reasoning;
8. trajectory/navigation;
9. temporal change;
10. world-state prediction.

Include adversarial cases: wrong CRS, swapped axis order, stale sensor data, overlapping IDs, incomplete topology and plausible-but-invalid LLM plans.

## Minimum publishable experiment matrix

A journal-grade paper should contain controlled comparisons, not only demonstrations.

| Model | VFM structure | Topology | Time | Multimodal | Tools | Validator |
|---|---:|---:|---:|---:|---:|---:|
| Base LLM | no | no | no | no | no | no |
| Geo-DAPT | no | no | no | no | no | no |
| VFM-Text | yes | no | no | no | no | no |
| VFM-Graph | yes | yes | no | no | no | no |
| VFM-Agent | yes | yes | yes | no | yes | yes |
| VFM-SpatialLM | yes | yes | yes | yes | yes | yes |

Required ablations:

- remove topology;
- remove temporal information;
- remove stable IDs;
- remove provenance;
- replace geographic holdout with random split;
- disable deterministic validator;
- disable modality alignment.

## Publication strategy

A strong paper should make **one central claim**, for example:

> A standardized spatiotemporal training substrate with explicit identity, topology, time and provenance improves cross-task spatial generalization and tool-grounded reliability compared with text-only geographic domain adaptation.

Do not claim a universal world model until state prediction, embodied transfer and closed-loop experiments are demonstrated.
