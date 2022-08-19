from typing import Dict, List

import numpy as np
import orjson


def index(path: str, key_id: str = "id") -> Dict:
    index = {}  # Init index dictionary

    with open(path, "rb") as file:
        position = file.tell()  # Init position

        for line in file:
            idx = orjson.loads(line)[key_id]
            index[idx] = position
            position = file.tell()  # Update position

    return index


def get(path: str, index: Dict, idx: str) -> Dict:
    with open(path, "rb") as file:
        position = index[idx]
        file.seek(position)
        line = file.readline()

    return orjson.loads(line)  # Convert line to Python Dictionary


def mget(path: str, index: Dict, indices: str) -> List[Dict]:
    positions = np.array([index[idx] for idx in indices])
    sorting_indices = np.argsort(positions)

    lines = [None] * len(positions)

    with open(path, "rb") as file:
        for i in sorting_indices:
            file.seek(positions[i])
            lines[i] = file.readline()

    return [orjson.loads(line) for line in lines]
