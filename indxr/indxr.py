import os
from typing import Callable, Dict, List, Tuple, Union

import numpy as np
import orjson

from .handlers import (
    csv_handler,
    custom_handler,
    jsonl_handler,
    numpy_handler,
    txt_handler,
)


class Indxr:
    def __init__(
        self, path: str, kind="infer", callback: Callable = None, **kwargs: Dict
    ):
        # Init  ----------------------------------------------------------------
        self.kind = kind
        self.path = path
        self.kwargs = kwargs
        self.callback = callback
        self.index = None  # Dict : k -> file position
        self.index_keys = None  # List of index keys

        # Infer file extension -------------------------------------------------
        if self.kind == "infer":
            self.kind = os.path.splitext(self.path)[1][1:]

        if self.kind not in {"txt", "jsonl", "csv", "tsv", "custom", "dat"}:
            raise NotImplementedError(
                f"Specified `kind` not supported. {self.kind}"
            )

        # Init kwargs ----------------------------------------------------------
        if not self.kwargs:
            self.kwargs = {}

        if "delimiter" not in self.kwargs:
            self.kwargs["delimiter"] = "\t" if self.kind == "tsv" else ","

        if "fieldnames" not in self.kwargs:
            self.kwargs["fieldnames"] = None

        if "has_header" not in self.kwargs:
            self.kwargs["has_header"] = True

        if "return_dict" not in self.kwargs:
            self.kwargs["return_dict"] = True

        if "key_id" not in self.kwargs:
            self.kwargs["key_id"] = "id"

        # Create index ---------------------------------------------------------
        self.index = self.create_index()
        self.index_keys = list(self.index)

    def create_index(self) -> Dict:
        if self.kind == "txt":
            return txt_handler.index(self.path)

        elif self.kind == "jsonl":
            return jsonl_handler.index(self.path, self.kwargs["key_id"])

        elif self.kind in {"csv", "tsv"}:
            fieldnames, index = csv_handler.index(self.path, **self.kwargs)
            self.kwargs["fieldnames"] = fieldnames
            return index

        elif self.kind == "dat":
            return numpy_handler.index(
                self.kwargs["dtype"], self.kwargs["shape"]
            )

        elif self.kind == "custom":
            return custom_handler.index(self.path)

        raise NotImplementedError("Specified `kind` not supported.")

    def get(self, idx: Union[str, int]) -> Union[str, Dict, np.ndarray]:
        if self.kind == "txt":
            x = txt_handler.get(path=self.path, index=self.index, idx=idx)

        elif self.kind == "jsonl":
            x = jsonl_handler.get(path=self.path, index=self.index, idx=idx)

        elif self.kind in {"csv", "tsv"}:
            x = csv_handler.get(
                path=self.path,
                index=self.index,
                idx=idx,
                delimiter=self.kwargs["delimiter"],
                fieldnames=self.kwargs["fieldnames"],
                return_dict=self.kwargs["return_dict"],
            )

        elif self.kind == "dat":
            x = numpy_handler.get(
                path=self.path, index=self.index, idx=str(idx)
            )

        elif self.kind == "custom":
            x = custom_handler.get(path=self.path, index=self.index, idx=idx)

        else:
            raise NotImplementedError()

        return self.callback(x) if self.callback else x

    def mget(self, indices: List[str]) -> List[Union[str, Dict, np.ndarray]]:
        if self.kind == "txt":
            xs = txt_handler.mget(
                path=self.path, index=self.index, indices=indices
            )

        elif self.kind == "jsonl":
            xs = jsonl_handler.mget(
                path=self.path, index=self.index, indices=indices
            )

        elif self.kind in {"csv", "tsv"}:
            xs = csv_handler.mget(
                path=self.path,
                index=self.index,
                indices=indices,
                delimiter=self.kwargs["delimiter"],
                fieldnames=self.kwargs["fieldnames"],
                return_dict=self.kwargs["return_dict"],
            )

        elif self.kind == "dat":
            xs = numpy_handler.mget(
                path=self.path,
                index=self.index,
                indices=[str(idx) for idx in indices],
            )

        elif self.kind == "custom":
            xs = custom_handler.mget(
                path=self.path, index=self.index, indices=indices
            )

        else:
            raise NotImplementedError()

        return [self.callback(x) for x in xs] if self.callback else xs

    def get_slice(self, start: int, stop: int) -> np.ndarray:
        if self.kind == "dat":
            return numpy_handler.get_slice(
                path=self.path, index=self.index, start=start, stop=stop
            )

        else:
            raise NotImplementedError()

    def mget_slice(self, slices: List[Tuple[int]]) -> List[np.ndarray]:
        if self.kind == "dat":
            return numpy_handler.mget_slice(
                path=self.path, index=self.index, slices=slices
            )

        else:
            raise NotImplementedError()

    def write(self, path: str):
        with open(path, "wb") as f:
            f.write(
                orjson.dumps(
                    {
                        "path": self.path,
                        "kind": self.kind,
                        "kwargs": self.kwargs,
                        "index": self.index,
                        "index_keys": self.index_keys,
                    },
                    option=orjson.OPT_INDENT_2,
                )
            )

    @staticmethod
    def read(path: str, callback: Callable = None):
        with open(path, "rb") as f:
            x = orjson.loads(f.read())

        if "shape" in x["kwargs"]:
            x["kwargs"]["shape"] = tuple(x["kwargs"]["shape"])

        indxr = Indxr(path=x["path"], kind=x["kind"], **x["kwargs"])
        indxr.index = x["index"]
        indxr.index_keys = x["index_keys"]
        indxr.callback = callback

        return indxr

    def __getitem__(self, idx: int) -> Union[str, Dict]:
        return self.get(self.index_keys[idx])

    def __len__(self) -> int:
        return len(self.index_keys)
