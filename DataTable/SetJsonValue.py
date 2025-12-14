# json_table.py
# -*- coding: utf-8 -*-

import json
import os
from typing import Any, List


def find_json_files(root_dir: str, recursive=True) -> List[str]:
    json_files = []

    if recursive:
        for root, _, files in os.walk(root_dir):
            for f in files:
                if f.lower().endswith(".json"):
                    json_files.append(os.path.join(root, f))
    else:
        for f in os.listdir(root_dir):
            if f.lower().endswith(".json"):
                json_files.append(os.path.join(root_dir, f))

    return json_files

class JsonTable:
    def __init__(self, json_path: str):
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON not found: {json_path}")

        self.json_path = json_path
        self.data = self._load()

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------
    def _load(self) -> list:
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _find_row(self, row_name: str) -> dict | None:
        for row in self.data:
            if row.get("Name") == row_name:
                return row
        return None

    def _walk_path(self, root: dict, path: List[str], create=False):
        cur = root
        for key in path[:-1]:
            if key not in cur:
                if not create:
                    return None
                cur[key] = {}
            cur = cur[key]
            if not isinstance(cur, dict):
                return None
        return cur

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------
    def get(self, row_name: str, path: List[str], default=None) -> Any:
        """
        Example:
            get("NewRow", ["Life", "Time", "Event"])
        """
        row = self._find_row(row_name)
        if not row:
            return default

        cur = row
        for key in path:
            if not isinstance(cur, dict) or key not in cur:
                return default
            cur = cur[key]
        return cur

    def set(self, row_name: str, path: List[str], value: Any) -> bool:
        """
        Example:
            set("NewRow", ["Life", "Time", "Event"], "xxx")
        """
        row = self._find_row(row_name)
        if not row:
            return False

        parent = self._walk_path(row, path, create=True)
        if parent is None:
            return False

        parent[path[-1]] = value
        return True

    def save(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------
    def rows(self) -> list[str]:
        return [row.get("Name") for row in self.data]


# ------------------------------------------------------
# Example
# ------------------------------------------------------

from PickleData.KeyValueStore import KeyValueStore
store = KeyValueStore()

from Json.JsonTable import find_json_files
json_dir = r"Z:/Projects/GameClient/Python/DT_Audio"
json_files = find_json_files(json_dir)



if __name__ == "__main__":

    tables = []
    for path in json_files:
        try:
            table = JsonTable(path)
            tables.append(table)
            for row in table.rows():
                event = table.get(row, ["Life", "Time", "Event"])
                print("Event:", event)
                print(store.get(event))
                table.set(
                    row,
                    ["Life", "Time", "Event"],
                    store.get(event)
                )
                table.save()
        except Exception as e:
            print(f"[Skip] {path} -> {e}")



