import os
from typing import List

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
