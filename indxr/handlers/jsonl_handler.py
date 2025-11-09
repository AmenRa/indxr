from io import BufferedReader

import numpy as np
import orjson


def index(path: str, key_id: str = "id") -> dict:
    index = {}  # Init index dictionary

    with open(path, "rb") as file:
        position = file.tell()  # Init position

        for line in file:
            idx = orjson.loads(line)[key_id]
            index[idx] = position
            position = file.tell()  # Update position

    return index


def get(file: BufferedReader, index: dict, idx: str) -> dict:
    position = index[idx]
    file.seek(position)
    line = file.readline()

    return orjson.loads(line)  # Convert line to Python dictionary


def mget(file: BufferedReader, index: dict, indices: str) -> list[dict]:
    positions = np.array([index[idx] for idx in indices])
    sorting_indices = np.argsort(positions)

    lines = [None] * len(positions)

    for i in sorting_indices:
        file.seek(positions[i])
        lines[i] = file.readline()

    return [orjson.loads(line) for line in lines]
