from gisgpt.tasks import build_instruction_examples
from gisgpt.vfm_schema import VFMManifest


def test_manifest_and_tasks():
    payload = {
        "dataset_id": "d",
        "sample_id": "s",
        "crs": {"code": "32648"},
        "assets": [{"id": "g", "modality": "vector", "uri": "x.parquet"}],
        "entities": [
            {"id": "a", "type": "building", "geometry_ref": "g", "bbox": [0, 1, 1, 2]},
            {"id": "b", "type": "road", "bbox": [0, 0, 1, 0.5]},
        ],
        "relations": [{"subject": "a", "predicate": "north_of", "object": "b"}],
    }
    manifest = VFMManifest.model_validate(payload)
    tasks = build_instruction_examples(manifest)
    assert tasks[0]["output"]["predicate"] == "north_of"
    assert any(t["task"] == "tool_plan" for t in tasks)
