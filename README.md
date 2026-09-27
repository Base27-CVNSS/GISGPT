# GISGPT — VFM-native Spatial Foundation Model Research Scaffold

> **Working research name:** **VFM-SpatialLM**  
> A reproducible research framework for learning spatial intelligence from standardized geospatial, BIM, 3D, sensor and trajectory data while keeping deterministic GIS computation outside the language model.

## Why this repository exists

This project takes inspiration from **BB-GeoGPT**'s two-stage idea (geographic domain adaptation + supervised instruction tuning), but changes the research target from *GIS question answering* to a broader **spatiotemporal world representation and tool-grounded reasoning** problem.

The central thesis is:

```text
Raw spatial data
  ↓
Digitization / normalization / QA-QC
  ↓
VFM canonical dataset
  ↓
Spatial pretraining + instruction tuning + multimodal alignment
  ↓
VFM-SpatialLM
  ↓
Tool-grounded GIS / BIM / Digital Twin / Robotics / GeoAI
```

The model is **not** expected to replace GIS engines. It should learn *intent, spatial semantics, relations, planning, tool selection and explanation*, while deterministic engines remain responsible for coordinate transforms, topology, geometry, routing, raster algebra and numerical computation.

## Naming note

The names **SpatialLM** and **SpatialLLM** are already used in published research. This repository therefore uses **VFM-SpatialLM** as a provisional project name. A journal submission should keep a distinct name to avoid confusion with prior work.

## Core design

```text
                           ┌──────────────────────┐
                           │ Natural-language goal│
                           └──────────┬───────────┘
                                      ↓
                           ┌──────────────────────┐
                           │ Spatial planner / LLM│
                           └──────────┬───────────┘
                                      ↓
                     ┌────────────────────────────────┐
                     │ Capability + tool router       │
                     └──────────┬─────────────────────┘
                                ↓
      ┌─────────────────────────────────────────────────────────┐
      │ Deterministic execution layer                           │
      │ GDAL · PROJ · GEOS · PostGIS · GeoPandas · OSMnx · IFC │
      └─────────────────────────┬───────────────────────────────┘
                                ↓
                  ┌──────────────────────────────┐
                  │ VFM validation / provenance │
                  └─────────────┬────────────────┘
                                ↓
                  ┌──────────────────────────────┐
                  │ Critic / explanation / agent│
                  └──────────────────────────────┘
```

## VFM as the training substrate

In this project, **VFM** is treated as a canonical multimodal spatial dataset contract, not merely a map file.

A VFM sample may bind:

- stable object/entity IDs;
- 2D/3D geometry and coordinate reference systems;
- raster/image observations;
- LiDAR/point clouds;
- BIM/IFC entities and meshes;
- trajectories and poses;
- time-indexed object states;
- sensor observations;
- topology and object relations;
- semantic labels and external vocabularies;
- spatial/temporal indexes;
- provenance, licensing and transformation history;
- train/validation/test split metadata.

This makes the same normalized sample usable by GIS, BIM, GeoAI, Digital Twin, SLAM, LiDAR, drones, autonomous vehicles and robots.

## Training stages

### Stage A — VFM canonicalization
Convert heterogeneous inputs into validated VFM manifests/chunks with stable IDs, CRS, temporal references, provenance and leakage-safe split keys.

### Stage B — Spatial domain-adaptive pretraining
Train on spatial language, structured object graphs, serialized topology, map/BIM metadata, coordinate-aware descriptions and tool documentation.

### Stage C — Spatial instruction tuning
Train `problem → goal → intent → capability → workflow → tool → validate → result` examples.

### Stage D — Multimodal alignment
Attach encoders/adapters for raster, point cloud, BIM/mesh, trajectories and sensor streams. The LLM consumes learned spatial tokens plus VFM metadata rather than flattening every modality into plain text.

### Stage E — Tool-grounded agent training
Teach the model to call deterministic spatial tools and to reject invalid plans before execution.

## Repository layout

```text
GISGPT/
├─ src/gisgpt/
│  ├─ vfm_schema.py          # canonical VFM manifest schema
│  ├─ validator.py           # structural + leakage checks
│  └─ tasks.py               # spatial instruction generation
├─ scripts/
│  ├─ build_vfm_dataset.py
│  ├─ generate_spatial_tasks.py
│  └─ validate_vfm.py
├─ configs/
│  ├─ pretrain.yaml
│  └─ sft.yaml
├─ examples/
│  └─ sample.vfm.json
├─ docs/
│  ├─ VFM_DATASET_SPEC.md
│  ├─ PAPER_Q1_DRAFT.md
│  └─ RESEARCH_ROADMAP.md
└─ tests/
   └─ test_vfm.py
```

## Quick start

```bash
python -m pip install -e .
python scripts/validate_vfm.py examples/sample.vfm.json
python scripts/generate_spatial_tasks.py examples/sample.vfm.json /tmp/vfm_tasks.jsonl
```

## Research questions

1. Does VFM-based canonicalization improve spatial reasoning compared with text-only GIS domain adaptation?
2. Which representation contributes most: geometry, topology, time, semantics, sensor state or provenance?
3. Does tool-grounded training reduce CRS, distance, topology and hallucinated-operation errors?
4. Can one VFM representation transfer across GIS, BIM, Digital Twin and embodied robotics?
5. How much spatial leakage occurs when random splits are replaced by geographic + temporal holdouts?

## Evaluation philosophy

Do not report only general QA accuracy. A credible spatial model should be evaluated on:

- qualitative spatial relation accuracy;
- metric distance/area tolerance;
- CRS selection and unit correctness;
- topological predicate accuracy;
- map/tool API planning success;
- executable GIS workflow success;
- spatial-temporal generalization;
- multimodal grounding;
- provenance fidelity;
- calibration / abstention;
- latency, memory and training cost.

Recommended external benchmarks include MapEval, GeoAnalystBench, PANGAEA/GEO-Bench-style geospatial evaluation and task-specific 3D/point-cloud benchmarks.

## Relationship to BB-GeoGPT

BB-GeoGPT is an important precursor: it curates geographic pretraining data and supervised GIS instructions, then adapts a general-domain LLM. This repository adopts that high-level learning strategy but **does not copy BB-GeoGPT training data**. The new research contribution proposed here is VFM-native multimodal standardization, leakage-safe spatiotemporal training, deterministic tool grounding and cross-domain GIS–BIM–Digital-Twin–robotics transfer.

Reference:

- Zhang, Y. et al. (2024). *BB-GeoGPT: A framework for learning a large language model for geographic information science*. Information Processing & Management, 61(5), 103808. https://doi.org/10.1016/j.ipm.2024.103808

## Research status

This repository is a **research scaffold**, not a claim of a completed foundation model. The paper draft contains hypotheses, methods and planned experiments; empirical result tables are intentionally left unfilled until experiments are executed.

## License and data governance

Code is intended to remain separable from dataset/model licenses. Every VFM dataset manifest should record source, license, consent/restriction flags and transformation provenance. Do not ingest restricted, personal or proprietary spatial data without a lawful basis and explicit governance.
