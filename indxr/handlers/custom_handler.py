from typing import Dict, List

import numpy as np


def index(path: str) -> Dict:
    index = {}  # Init index dictionary

    with open(path, "rb") as file:
        position = file.tell()  # Init position

        for i, _ in enumerate(file):
            index[str(i)] = position
            position = file.tell()  # Update position

    return index


def get(path: str, index: Dict, idx: int) -> bytes:
    print("ok")
    with open(path, "rb") as file:
        position = index[idx]
        file.seek(position)
        line = file.readline()

    return line.strip()


def mget(path: str, index: Dict, indices: str) -> List[bytes]:
    positions = np.array([index[idx] for idx in indices])
    sorting_indices = np.argsort(positions)

    lines = [None] * len(positions)

    with open(path, "rb") as file:
        for i in sorting_indices:
            file.seek(positions[i])
            lines[i] = file.readline()

    return [line.strip() for line in lines]
