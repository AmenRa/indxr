from io import BufferedReader

import numpy as np


def index(path: str) -> dict:
    index = {}  # Init index dictionary

    with open(path, "rb") as file:
        position = file.tell()  # Init position

        for i, _ in enumerate(file):
            index[str(i)] = position
            position = file.tell()  # Update position

    return index


def get(file: BufferedReader, index: dict, idx: str) -> str:
    position = index[idx]
    file.seek(position)
    line = file.readline()

    return line.decode("utf-8").strip()


def mget(file: BufferedReader, index: dict, indices: str) -> list[str]:
    positions = np.array([index[idx] for idx in indices])
    sorting_indices = np.argsort(positions)

    lines = [None] * len(positions)

    for i in sorting_indices:
        file.seek(positions[i])
        lines[i] = file.readline()

    return [line.decode("utf-8").strip() for line in lines]
