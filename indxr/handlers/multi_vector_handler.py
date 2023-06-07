import re
from typing import Dict, List, Tuple

import numpy as np


def get_itemsize(dtype: str):
    return int(re.sub("\D", "", dtype)) // 8


def index(dtype: str, shape: Tuple[int], mapping: Dict) -> Dict:
    step = shape[1] * get_itemsize(dtype)
    index = {k: v["offset"] * step for k, v in mapping.items()}
    index["dim"] = shape[1]
    index["dtype"] = dtype
    return index


def get(path: str, index: Dict, mapping: Dict, idx: str) -> np.ndarray:
    return np.memmap(
        path,
        dtype=index["dtype"],
        mode="r",
        shape=(mapping[idx]["length"], index["dim"]),
        offset=index[idx],
    )


def mget(path: str, index: Dict, mapping: Dict, indices: List[str]) -> np.ndarray:
    return [get(path, index, mapping, idx) for idx in indices]
