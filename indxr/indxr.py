import json
from typing import List, Union

from .csv_handler import get_csv_line, index_csv
from .jsonl_handler import get_jsonl_line, index_jsonl, mget_jsonl_line
from .raw_handler import get_raw_line, index_raw


class Indxr:
    def __init__(self, kind: str, path: str, **kwargs: dict):
        if kind not in {"raw", "jsonl", "csv"}:
            raise NotImplementedError("Specified `kind` not supported.")

        self.kind = kind
        self.path = path
        self.kwargs = kwargs

        if not kwargs:
            self.kwargs = {}

        if "delimiter" not in self.kwargs:
            self.kwargs["delimiter"] = ","
        if "fieldnames" not in self.kwargs:
            self.kwargs["fieldnames"] = None
        if "has_header" not in self.kwargs:
            self.kwargs["has_header"] = True
        if "return_dict" not in self.kwargs:
            self.kwargs["return_dict"] = True
        if "key_id" not in self.kwargs:
            self.kwargs["key_id"] = "id"

        self.index = self.create_index()
        self.index_keys = list(self.index)

    def create_index(self) -> dict:
        if self.kind == "raw":
            return index_raw(self.path)

        elif self.kind == "jsonl":
            return index_jsonl(self.path, self.kwargs["key_id"])

        elif self.kind == "csv":
            fieldnames, index = index_csv(self.path, **self.kwargs)
            self.kwargs["fieldnames"] = fieldnames
            return index

        raise NotImplementedError("Specified `kind` not supported.")

    def get(self, idx: Union[str, int]) -> Union[str, dict]:
        if self.kind == "raw":
            return get_raw_line(path=self.path, index=self.index, idx=idx)

        elif self.kind == "jsonl":
            return get_jsonl_line(path=self.path, index=self.index, idx=idx)

        elif self.kind == "csv":
            return get_csv_line(
                path=self.path,
                index=self.index,
                idx=idx,
                delimiter=self.kwargs["delimiter"],
                fieldnames=self.kwargs["fieldnames"],
                return_dict=self.kwargs["return_dict"],
            )

        raise NotImplementedError("Specified `kind` not supported.")

    def mget(self, indices: List[str]):
        return mget_jsonl_line(
            path=self.path, index=self.index, indices=indices
        )

    def write(self, path: str):
        with open(path, "w") as f:
            f.write(
                json.dumps(
                    {
                        "kind": self.kind,
                        "path": self.path,
                        "kwargs": self.kwargs,
                        "index": self.index,
                    },
                    indent=4,
                )
            )

    @staticmethod
    def read(path: str):
        with open(path, "r") as f:
            x = json.loads(f.read())

        indxr = Indxr(kind=x["kind"], path=x["path"], **x["kwargs"])
        indxr.index = x["index"]

        return indxr

    def __getitem__(self, idx: int) -> Union[str, dict]:
        return self.get(self.index_keys[idx])

    def __len__(self) -> int:
        return len(self.index_keys)
