import re
from typing import Dict, List, Tuple

import numpy as np


def get_itemsize(dtype: str):
    return int(re.sub("\D", "", dtype)) // 8


def index(dtype: str, shape: Tuple[int]) -> Dict:
    step = shape[1] * get_itemsize(dtype)
    index = {str(i): i * step for i in range(shape[0])}
    index["dim"] = shape[1]
    index["dtype"] = dtype
    return index


def get(path: str, index: Dict, idx: str) -> np.ndarray:
    return np.memmap(
        path,
        dtype=index["dtype"],
        mode="r",
        shape=(1, index["dim"]),
        offset=index[idx],
    )[0]


def mget(path: str, index: Dict, indices: List[str]) -> np.ndarray:
    return np.asarray([get(path, index, idx) for idx in indices])


def get_slice(path: str, index: Dict, start: int, stop: int) -> np.ndarray:
    return np.memmap(
        path,
        dtype=index["dtype"],
        mode="r",
        shape=(stop - start, index["dim"]),
        offset=index[str(start)],
    )


def mget_slice(path: str, index: Dict, slices: List[Tuple[int]]) -> np.ndarray:
    return [get_slice(path, index, *slice) for slice in slices]
