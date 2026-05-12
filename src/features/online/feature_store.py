import json
from pathlib import Path
from typing import Any


class OnlineFeatureStore:
    """
    Simple mock online feature store backed by a JSON file.
    Good enough for local demo / architecture completeness.
    """

    def __init__(self, store_path: str = "artifacts/logs/online_feature_store.json"):
        self.store_path = Path(store_path)
        self.store_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.store_path.exists():
            self._write_store({})

    def _read_store(self) -> dict[str, Any]:
        with open(self.store_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_store(self, data: dict[str, Any]) -> None:
        with open(self.store_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def put(self, entity_id: str, feature_row: dict[str, Any]) -> None:
        store = self._read_store()
        store[str(entity_id)] = feature_row
        self._write_store(store)

    def get(self, entity_id: str) -> dict[str, Any] | None:
        store = self._read_store()
        return store.get(str(entity_id))

    def get_all(self) -> dict[str, Any]:
        return self._read_store()

    def delete(self, entity_id: str) -> None:
        store = self._read_store()
        store.pop(str(entity_id), None)
        self._write_store(store)