from pathlib import Path

from src.features.online.feature_store import OnlineFeatureStore


def test_online_feature_store_put_get(tmp_path: Path):
    store_file = tmp_path / "store.json"
    store = OnlineFeatureStore(str(store_file))

    row = {"encounter_id": 1, "race": "Caucasian", "age": "[70-80)"}
    store.put("1", row)

    loaded = store.get("1")
    assert loaded is not None
    assert loaded["race"] == "Caucasian"