# VFM-SpatialLM: A Standardized Spatiotemporal Data Substrate for Tool-Grounded Geospatial Foundation Models and Embodied Digital Twins

**Manuscript status:** research proposal / Q1-oriented scaffold.  
**Important:** no empirical values are claimed in this draft. Result tables must be populated only after reproducible experiments.

## Abstract

Large language models have stimulated rapid progress in geographic question answering, GIS code generation and autonomous geospatial workflows, yet current approaches frequently conflate linguistic reasoning with deterministic spatial computation and rely on training corpora whose geometric reference systems, object identities, temporal scope and provenance are weakly standardized. Meanwhile, emerging spatial foundation models for remote sensing, 3D point clouds, urban intelligence and embodied agents operate on heterogeneous data representations that are difficult to align across GIS, Building Information Modeling (BIM), Internet of Things (IoT), digital twins, simultaneous localization and mapping (SLAM), LiDAR, drones, autonomous vehicles and robotics. This paper proposes **VFM-SpatialLM**, a research framework in which a VFM canonical dataset layer standardizes object identity, geometry, coordinate reference systems, topology, time, multimodal observations, provenance and leakage-safe split metadata before model training. The framework separates a language-based planner from deterministic GIS/BIM execution and validation, then extends geographic domain-adaptive pretraining and supervised instruction tuning with cross-modal alignment and optional world-state prediction objectives. We formulate a benchmark protocol spanning spatial relations, CRS reasoning, executable GIS workflows, 3D grounding, BIM relations, trajectory reasoning, temporal change and next-state prediction. The study is designed around controlled baselines and ablations to determine which VFM components contribute to generalization and reliability. Rather than treating the LLM as a geometry engine, the proposed architecture positions it as a semantic planner embedded within a verifiable spatial computing system. The resulting research agenda aims to provide a reproducible path from GIS-specific language models toward interoperable spatial intelligence for geospatial digital twins and embodied systems.

**Keywords:** geospatial foundation model; spatial reasoning; large language model; GIS; BIM; digital twin; VFM; LiDAR; SLAM; robotics; tool use; multimodal learning.

## 1. Introduction

Geospatial AI is moving from task-specific predictive models toward foundation models and language-driven systems capable of interpreting user intent, synthesizing workflows and interacting with external tools. BB-GeoGPT demonstrated a practical two-stage route for adapting a general language model to geographic information science through geographic-domain pretraining data and supervised fine-tuning instructions. Subsequent benchmark work has shown, however, that general-purpose foundation models remain unreliable on map-based spatial reasoning and executable geoprocessing. In parallel, recent 3D spatial language models process point clouds and produce structured scene representations, while urban spatial-intelligence frameworks increasingly fuse multimodal geographic data.

These developments expose a missing layer. Model architectures are advancing faster than the standardization of the **training object itself**. A road may appear as a vector feature, pixels in an orthophoto, points in LiDAR, an IFC-aligned infrastructure element, a trajectory constraint and a time-varying sensor context. If those observations are linked only by filenames or weak metadata, a model cannot reliably learn that they describe the same physical entity. Coordinate systems, local sensor frames, timestamps, topology and provenance further complicate the problem.

We therefore ask whether a canonical spatiotemporal data substrate can improve both learning and system reliability. We introduce the VFM training profile as a layer that binds heterogeneous modality assets to stable entities and explicit spatial-temporal relations. On top of this substrate, VFM-SpatialLM is designed to learn semantic and planning capabilities while delegating metric geometry and geoprocessing to deterministic tools.

The proposed contribution is not another claim that an LLM can replace GIS. Instead, it is a hypothesis about **representation and system decomposition**: spatial intelligence may improve when learning is grounded in standardized object identity, topology, time, reference frames and provenance, and when computation that has exact algorithms remains externally verifiable.

## 2. Related Work

### 2.1 GIS-specific language models

BB-GeoGPT provides the principal conceptual starting point for this work. It curates geographic pretraining and supervised instruction datasets and adapts a general-domain LLM in two stages. This establishes that domain adaptation can improve geographic language capability, but it does not solve the broader problem of a shared multimodal physical-world representation.

### 2.2 Spatial reasoning benchmarks

MapEval evaluates textual, API-based and visual map reasoning and reports substantial gaps between foundation models and human performance. GeoAnalystBench emphasizes executable spatial-analysis workflows and code-generation quality. These benchmarks motivate evaluation beyond conventional question answering.

### 2.3 Geospatial foundation models

Remote-sensing foundation models increasingly span sensors, resolutions and temporal contexts. PANGAEA and GEO-Bench-style protocols highlight that broad pretraining does not guarantee consistent superiority and that capability-specific, reproducible evaluation is necessary.

### 2.4 3D spatial language models

SpatialLM (Mao et al., 2025) processes 3D point clouds and predicts structured indoor layouts and object boxes, showing that multimodal LLMs can learn structured 3D outputs. Its focus is primarily indoor 3D reconstruction/understanding rather than GIS-scale spatiotemporal interoperability.

A separate 2026 work named SpatialLLM targets multimodal urban spatial intelligence. Because both **SpatialLM** and **SpatialLLM** are established names, the present work uses **VFM-SpatialLM** as a distinct working title.

### 2.5 BIM and digital twins

IFC provides an open international standard for BIM information exchange. CityGML provides a semantic model for 3D urban objects and explicitly supports smart-city/digital-twin use cases. OGC SensorThings provides a standardized way to connect observations and taskable IoT systems. These standards should be interoperated with rather than replaced.

## 3. Problem Formulation

Let a physical scene at time (t) contain a set of entities (E_t), geometry (G_t), topology (R_t), semantic attributes (S_t), multimodal observations (O_t), sensor/agent poses (P_t), and provenance (V_t).

We define a canonical sample:

[
X_t = (E_t, G_t, R_t, S_t, O_t, P_t, T_t, V_t)
]

where (T_t) denotes temporal/reference metadata.

The research objective is not to force all components into text. Instead, modality-specific encoders produce representations that are aligned through shared entity IDs and frame transforms.

For tool-grounded reasoning, a user request (q) is mapped to:

[
q ightarrow I ightarrow W ightarrow C ightarrow A
]

where (I) is spatial intent, (W) is a workflow, (C) is a typed capability/tool call, and (A) is the deterministic execution result. A validator (D) checks invariants before the result is explained by the model:

[
D(A, X_t) ightarrow {valid, invalid, uncertain}
]

For world-model experiments, an optional dynamics component predicts:

[
hat{X}_{t+1} = F(X_t, a_t)
]

where (a_t) is an agent action or environmental transition. This objective is evaluated independently from language generation.

## 4. VFM Canonical Training Profile

### 4.1 Stable identity

Every physical/logical object receives a stable entity identifier. Modality assets reference entities rather than relying on filenames.

### 4.2 Spatial reference and frames

Every geometry or observation must expose CRS or local-frame information, units, axis order and the transform required to align it to a world frame.

### 4.3 Topology

Topological, network, BIM and qualitative relations are represented explicitly as auditable triples. Computed relations retain evidence/derivation metadata.

### 4.4 Time

Samples distinguish acquisition time, valid time, trajectory order and state transitions.

### 4.5 Provenance

Data source, license, transformations, annotation process and hashes are treated as first-class training metadata.

### 4.6 Leakage-safe split keys

Benchmark partitions are built by geographic, temporal, scene and source groups. Random feature splitting is used only as a diagnostic baseline, not as the principal generalization claim.

## 5. Proposed Model Architecture

The architecture contains five separable subsystems.

**Spatial language backbone.** A configurable open LLM provides language understanding and generation.

**Modality encoders.** Raster, point-cloud, BIM graph, trajectory and sensor encoders generate modality-specific latent tokens.

**VFM alignment layer.** Stable IDs, coordinate/frame metadata and time align modalities before fusion. Alignment may be implemented through projectors, cross-attention or query-former style interfaces.

**Tool router and deterministic executor.** Typed GIS/BIM capabilities invoke external engines for metric and topological computation.

**Validator/critic.** Deterministic checks verify geometry validity, CRS/units, schema, topology, provenance and workflow postconditions. A language critic may explain validation reports but is not the sole judge of correctness.

## 6. Training Strategy

### 6.1 Stage 1: geographic domain-adaptive pretraining

Continue training an open language model on clean geographic text, standards documentation, spatial metadata and structured VFM serializations.

### 6.2 Stage 2: spatial instruction tuning

Construct supervised examples for:

- intent parsing;
- relation reasoning;
- workflow decomposition;
- tool selection;
- CRS/unit diagnosis;
- provenance reasoning;
- error repair;
- result explanation.

### 6.3 Stage 3: multimodal alignment

Train projectors/encoders on VFM-linked pairs and groups: image↔entity, point cloud↔entity, BIM↔GIS object, trajectory↔scene and sensor↔feature-of-interest.

### 6.4 Stage 4: tool-grounded optimization

Optimize structured tool calls and executable workflow success. Preference or reinforcement learning may be investigated only after deterministic reward signals are defined.

### 6.5 Stage 5: optional world-state modeling

Add state-transition training for datasets with sufficient temporal density. Candidate objectives include next-state latent prediction, object-state change classification and trajectory-conditioned future occupancy. This stage should not be conflated with ordinary instruction tuning.

A composite research objective can be written as:

[
L = lambda_{lm}L_{lm} + lambda_{rel}L_{rel} +
    lambda_{align}L_{align} + lambda_{tool}L_{tool} +
    lambda_{state}L_{state}
]

Ablation experiments must estimate the contribution of each term rather than fixing all components at once.

## 7. Research Questions

**RQ1.** Does VFM canonicalization improve spatial reasoning over geographic text-only domain adaptation?

**RQ2.** Which VFM components—stable identity, topology, time, provenance or reference-frame metadata—contribute most to generalization?

**RQ3.** Does deterministic tool grounding reduce CRS, unit, topology and fabricated-operation errors?

**RQ4.** Can a common VFM representation support transfer across GIS, BIM, remote sensing, point-cloud and trajectory tasks?

**RQ5.** Does geographic/temporal leakage-safe evaluation materially change conclusions compared with random splits?

**RQ6.** Can VFM-linked temporal state sequences support measurable next-state/world-model capabilities useful to drones, vehicles and robots?

## 8. Experimental Design

### 8.1 Baselines

1. unadapted base LLM;
2. BB-GeoGPT-style geographic DAPT;
3. DAPT + conventional SFT;
4. VFM text-only serialization;
5. VFM + explicit topology;
6. VFM + tool grounding;
7. full VFM-SpatialLM multimodal model.

### 8.2 Ablations

Remove one factor at a time:

- stable IDs;
- CRS/frame metadata;
- topology;
- temporal context;
- provenance;
- multimodal alignment;
- deterministic validator.

### 8.3 Evaluation groups

**Spatial language:** qualitative direction and relation tasks.

**Metric spatial reasoning:** distance/area results checked against deterministic reference calculations.

**CRS competence:** correct projection/unit choice and axis-order robustness.

**Tool use:** syntactic validity, semantic validity, execution success and postcondition success.

**Map reasoning:** MapEval-style textual/API/visual tasks.

**Workflow generation:** GeoAnalystBench-style executable geoprocessing tasks.

**3D grounding:** indoor/outdoor point-cloud object/layout tasks.

**BIM:** IFC hierarchy, adjacency, containment and GIS↔BIM alignment.

**Trajectory/navigation:** relative pose, route constraints and traversability.

**Temporal/world state:** change detection and next-state prediction.

### 8.4 Metrics

Report task accuracy together with spatially meaningful measures:

- relation F1;
- distance/area error;
- topology violation rate;
- CRS/unit error rate;
- valid tool-call rate;
- executable workflow success;
- hallucinated entity/tool rate;
- calibration and abstention;
- geographic/temporal out-of-distribution gap;
- latency, tokens, VRAM and training compute.

## 9. GIS–BIM–Digital Twin–Embodied Integration

The proposed digital-twin stack is:

```text
Physical world
   ↓ sensing
camera / LiDAR / GNSS / IMU / IoT / drone
   ↓
SLAM / photogrammetry / detection / mapping
   ↓
VFM canonical state
   ↙          ↓           ↘
 GIS       BIM/IFC      3D scene
   ↘          ↓           ↙
       Digital Twin
            ↓
     VFM-SpatialLM
            ↓
 planner → tools → validator
            ↓
 robot / vehicle / drone / human decision
```

VFM acts as the exchange/training substrate. The LLM is one reasoning component inside the loop, not the digital twin itself.

## 10. Expected Contributions

If supported experimentally, the paper would contribute:

1. a canonical multimodal spatial training profile centered on identity, topology, time and provenance;
2. a tool-grounded spatial foundation-model architecture that separates semantic planning from deterministic GIS computation;
3. a leakage-safe benchmark protocol across GIS, BIM, 3D and embodied tasks;
4. empirical evidence identifying which data-standardization components drive spatial generalization;
5. an interoperability path from conventional geospatial datasets to digital-twin and world-model research.

## 11. Threats to Validity

The main threats include licensing bias in training data, geographic imbalance, annotation errors, CRS normalization mistakes, synthetic-to-real domain gaps, benchmark contamination, incomplete BIM/point-cloud alignment and over-attribution of performance gains to model architecture rather than dataset quality. World-model claims additionally require closed-loop or temporally grounded evaluation; language-only improvements are insufficient evidence.

## 12. Reproducibility Requirements

A publishable experiment should release or precisely document:

- VFM schema/version;
- dataset sources and licenses;
- conversion code;
- split-generation code;
- model checkpoint/base model;
- prompts and templates;
- training hyperparameters;
- random seeds;
- tool versions;
- CRS/coordinate processing;
- evaluation scripts;
- failed runs and excluded samples;
- hardware and compute budget.

## 13. Conclusion

The next step for LLMs in GIS should not be to teach a language model to imitate every spatial algorithm. A more defensible research direction is to standardize the spatial world presented to the model, train representations that connect language to entities and multimodal observations, and preserve deterministic geospatial computation as a verifiable external capability. VFM-SpatialLM formalizes this direction and extends it toward BIM, digital twins and embodied world models. The decisive scientific test is whether this representation produces measurable gains under geographic, temporal and cross-modal generalization—not whether a demonstration can generate an attractive map.

## References — seed list

1. Zhang, Y. et al. (2024). BB-GeoGPT: A framework for learning a large language model for geographic information science. *Information Processing & Management*, 61(5), 103808. https://doi.org/10.1016/j.ipm.2024.103808
2. Mao, Y. et al. (2025). SpatialLM: Training Large Language Models for Structured Indoor Modeling. arXiv:2506.07491; NeurIPS 2025.
3. Dihan, M. L. et al. (2025). MapEval: A Map-Based Evaluation of Geo-Spatial Reasoning in Foundation Models. *ICML 2025*, PMLR 267.
4. Zhang et al. (2025). GeoAnalystBench: A GeoAI Benchmark for Assessing Large Language Models for Spatial Analysis Workflow and Code Generation. *Transactions in GIS*.
5. Chen, J. et al. (2026). SpatialLLM: From multi-modality data to urban spatial intelligence. *International Journal of Applied Earth Observation and Geoinformation*, 147, 105177.
6. Open Geospatial Consortium. CityGML 3.0 Conceptual Model Standard.
7. Open Geospatial Consortium. SensorThings API Part 1: Sensing 1.1 and Part 2: Tasking Core.
8. buildingSMART International. IFC 4.3 / ISO 16739-1:2024.
9. PANGAEA benchmark for geospatial foundation models, *IEEE Geoscience and Remote Sensing Magazine* (2026).
10. UrbanGeoEval (2026), ACL 2026 long paper on city-scale geospatial reasoning.

### Recommended target venues

Potential scopes include *International Journal of Geographical Information Science*, *ISPRS Journal of Photogrammetry and Remote Sensing*, *International Journal of Applied Earth Observation and Geoinformation*, *Computers, Environment and Urban Systems*, *Automation in Construction* or a comparable journal. Journal quartiles and scope change over time and must be verified at submission.
