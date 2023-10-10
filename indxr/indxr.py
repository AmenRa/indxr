import os
from pathlib import Path
from typing import Callable, Dict, List, Tuple, Union

import numpy as np
import orjson

from .handlers import (
    csv_handler,
    custom_handler,
    jsonl_handler,
    multi_vector_handler,
    numpy_handler,
    txt_handler,
)


class Indxr:
    def __init__(
        self,
        path: Union[str, Path],
        kind: str = None,
        callback: Callable = None,
        **kwargs: Dict,
    ):
        """_summary_

        Args:
            path (Union[str, Path]): The path where the file to index is located.
            kind (str, optional): Kind of file to index, must be either "txt", "jsonl", "csv", "tsv", "custom", "dat". If None, it will be automatically inferred from the filename extension.
            callback (Callable, optional): A function to apply to an item when read. Defaults to None.

        Returns:
            Indxr: Indxr object.
        """
        # Init  ----------------------------------------------------------------
        self.kind = kind
        self.path = str(path)
        self.kwargs = kwargs
        self.callback = callback
        self.index = None  # Dict : k -> file position
        self.index_keys = None  # List of index keys
        self.iteration_index = 0  # Index for iteration
        self.file = open(path, "rb")  # File pointer

        # Infer file extension -------------------------------------------------
        if self.kind is None:
            self.kind = os.path.splitext(self.path)[1][1:]

        if self.kind not in {"txt", "jsonl", "csv", "tsv", "custom", "dat"}:
            raise NotImplementedError(f"Specified `kind` not supported. {self.kind}")

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
            if "mapping" in self.kwargs:
                return multi_vector_handler.index(
                    self.kwargs["dtype"],
                    self.kwargs["shape"],
                    self.kwargs["mapping"],
                )
            else:
                return numpy_handler.index(self.kwargs["dtype"], self.kwargs["shape"])

        elif self.kind == "custom":
            return custom_handler.index(self.path)

        raise NotImplementedError("Specified `kind` not supported.")

    def get(self, key: Union[str, int]) -> Union[str, Dict, np.ndarray]:
        """Get an item by key.

        Args:
            key (Union[str, int]): Key of the item to get.

        Returns:
            Union[str, Dict, np.ndarray]: Item.
        """
        if self.kind == "txt":
            x = txt_handler.get(file=self.file, index=self.index, idx=key)

        elif self.kind == "jsonl":
            x = jsonl_handler.get(file=self.file, index=self.index, idx=key)

        elif self.kind in {"csv", "tsv"}:
            x = csv_handler.get(
                file=self.file,
                index=self.index,
                idx=key,
                delimiter=self.kwargs["delimiter"],
                fieldnames=self.kwargs["fieldnames"],
                return_dict=self.kwargs["return_dict"],
            )

        elif self.kind == "dat":
            if "mapping" in self.kwargs:
                x = multi_vector_handler.get(
                    path=self.path,
                    index=self.index,
                    mapping=self.kwargs["mapping"],
                    idx=str(key),
                )
            else:
                x = numpy_handler.get(path=self.path, index=self.index, idx=str(key))

        elif self.kind == "custom":
            x = custom_handler.get(file=self.file, index=self.index, idx=key)

        else:
            raise NotImplementedError()

        return self.callback(x) if self.callback else x

    def mget(
        self, keys: Union[List[int], List[str]]
    ) -> List[Union[str, Dict, np.ndarray]]:
        """Get multiple item by key.

        Args:
            keys (Union[List[int], List[str]]): Keys of the items to get.

        Returns:
            List[Union[str, Dict, np.ndarray]]: items.
        """
        if self.kind == "txt":
            xs = txt_handler.mget(file=self.file, index=self.index, indices=keys)

        elif self.kind == "jsonl":
            xs = jsonl_handler.mget(file=self.file, index=self.index, indices=keys)

        elif self.kind in {"csv", "tsv"}:
            xs = csv_handler.mget(
                file=self.file,
                index=self.index,
                indices=keys,
                delimiter=self.kwargs["delimiter"],
                fieldnames=self.kwargs["fieldnames"],
                return_dict=self.kwargs["return_dict"],
            )

        elif self.kind == "dat":
            if "mapping" in self.kwargs:
                xs = multi_vector_handler.mget(
                    path=self.path,
                    index=self.index,
                    mapping=self.kwargs["mapping"],
                    indices=[str(idx) for idx in keys],
                )
            else:
                xs = numpy_handler.mget(
                    path=self.path,
                    index=self.index,
                    indices=[str(idx) for idx in keys],
                )

        elif self.kind == "custom":
            xs = custom_handler.mget(file=self.file, index=self.index, indices=keys)

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

    def write(self, path: Union[str, Path]):
        """Write index to file.

        Args:
            path (Union[str, Path]): Where to write the index.
        """
        with open(str(path), "wb") as f:
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
    def read(path: Union[str, Path], callback: Callable = None):
        """Read index form file.

        Args:
            path (Union[str, Path]): Where to write the index.
            callback (Callable, optional): A function to apply to an item when read. Defaults to None.

        Returns:
            Indxr: Indxr object.
        """
        with open(str(path), "rb") as f:
            x = orjson.loads(f.read())

        if "shape" in x["kwargs"]:
            x["kwargs"]["shape"] = tuple(x["kwargs"]["shape"])

        indxr = Indxr(path=x["path"], kind=x["kind"], **x["kwargs"])
        indxr.index = x["index"]
        indxr.index_keys = x["index_keys"]
        indxr.callback = callback

        return indxr

    def generate_batches(self, batch_size: int, shuffle: bool = False):
        """Batch generator.

        Args:
            batch_size (int): Batch size.
            shuffle (bool, optional): Whether to shuffle the data. Defaults to False.

        Yields:
            List[Union[str, Dict, np.ndarray]]: Batch of items.
        """
        indices = np.arange(len(self))

        if shuffle:
            np.random.shuffle(indices)

        for i in range(0, len(self), batch_size):
            keys = [self.index_keys[key] for key in indices[i : i + batch_size]]
            yield self.mget(keys)

    def __getitem__(self, key: Union[int, slice]) -> Union[str, Dict]:
        # Handle single-item access
        if not isinstance(key, slice):
            return self.get(self.index_keys[key])

        # Handle slicing
        start = key.start if key.start is not None else 0
        stop = key.stop if key.stop is not None else len(self)
        step = key.step if key.step is not None else 1
        keys = [self.index_keys[i] for i in range(start, stop, step)]
        return self.mget(keys)

    def __len__(self) -> int:
        return len(self.index_keys)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iteration_index >= len(self):
            raise StopIteration
        result = self.get(self.index_keys[self.iteration_index])
        self.iteration_index += 1
        return result

    def __del__(self):
        self.file.close()
