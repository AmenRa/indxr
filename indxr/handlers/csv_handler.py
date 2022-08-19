from csv import reader
from typing import Dict, List

import numpy as np


def csv_line_to_dict(line: str, fieldnames: List, delimiter: str) -> Dict:
    return dict(
        zip(
            fieldnames,
            list(reader([line.decode("utf-8")], delimiter=delimiter))[0],
        )
    )


def csv_line_to_list(line: str, delimiter: str) -> List:
    return list(reader([line.decode("utf-8")], delimiter=delimiter))[0]


def index(
    path: str,
    delimiter: str = ",",
    fieldnames: List = None,
    has_header: bool = True,
    return_dict: bool = True,
    key_id: str = "id",
) -> Dict:
    assert (
        fieldnames or has_header
    ), "File must have header or fieldnames must be defined by user"

    index = {}

    with open(path, "rb") as file:
        position = file.tell()  # Init position

        for i, line in enumerate(file):
            if i == 0 and has_header:
                if not fieldnames:
                    fieldnames = line.decode("utf-8").strip().split(delimiter)

            elif return_dict:
                idx = csv_line_to_dict(
                    line=line, fieldnames=fieldnames, delimiter=delimiter
                )[key_id]
                index[idx] = position

            else:
                index[i] = position

            position = file.tell()  # Update position

    return fieldnames, index


def get(
    path: str,
    index: dict,
    idx: str,
    delimiter: str = ",",
    fieldnames: List = None,
    return_dict: bool = True,
) -> Dict:
    with open(path, "rb") as file:
        position = index[idx]
        file.seek(position)
        line = file.readline()

    return (
        csv_line_to_dict(line=line, fieldnames=fieldnames, delimiter=delimiter)
        if return_dict
        else csv_line_to_list(line=line, delimiter=delimiter)
    )


def mget(
    path: str,
    index: dict,
    indices: str,
    delimiter: str = ",",
    fieldnames: List = None,
    return_dict: bool = True,
) -> List[Dict]:
    positions = np.array([index[idx] for idx in indices])
    sorting_indices = np.argsort(positions)

    lines = [None] * len(positions)

    with open(path, "rb") as file:
        for i in sorting_indices:
            file.seek(positions[i])
            lines[i] = file.readline()

    if return_dict:
        return [
            csv_line_to_dict(
                line=line, fieldnames=fieldnames, delimiter=delimiter
            )
            for line in lines
        ]

    return [csv_line_to_list(line=line, delimiter=delimiter) for line in lines]
