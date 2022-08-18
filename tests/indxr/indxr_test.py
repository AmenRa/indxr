import os

import pytest

from indxr import Indxr

# FIXTURES =====================================================================

# TESTS ========================================================================
def test_raw_index():
    index = Indxr("raw", "tests/test_data/sample.txt")

    assert index.get("0") == "this is line 0"
    assert index.get("1") == "this is line 1"
    assert index.get("2") == "this is line 2"


def test_jsonl_index():
    index = Indxr("jsonl", "tests/test_data/sample.jsonl")

    assert index.get("id_0") == {"id": "id_0", "content": "this is line 0"}
    assert index.get("id_1") == {"id": "id_1", "content": "this is line 1"}
    assert index.get("id_2") == {"id": "id_2", "content": "this is line 2"}

    assert index.mget(["id_0", "id_1", "id_2"]) == [
        {"id": "id_0", "content": "this is line 0"},
        {"id": "id_1", "content": "this is line 1"},
        {"id": "id_2", "content": "this is line 2"},
    ]
    assert index.mget(["id_2", "id_0", "id_1"]) == [
        {"id": "id_2", "content": "this is line 2"},
        {"id": "id_0", "content": "this is line 0"},
        {"id": "id_1", "content": "this is line 1"},
    ]


def test_csv_index_w_header():
    index = Indxr("csv", "tests/test_data/sample_w_header.csv")

    assert index.get("0") == {"id": "0", "content": "this is line 0"}
    assert index.get("1") == {"id": "1", "content": "this is line 1"}
    assert index.get("2") == {"id": "2", "content": "this is line 2"}


def test_csv_index_wo_header():
    index = Indxr(
        "csv",
        "tests/test_data/sample_wo_header.csv",
        fieldnames=["new_id", "content"],
        has_header=False,
        key_id="new_id",
    )

    assert index.get("0") == {"new_id": "0", "content": "this is line 0"}
    assert index.get("1") == {"new_id": "1", "content": "this is line 1"}
    assert index.get("2") == {"new_id": "2", "content": "this is line 2"}


def test_tsv_index_w_header():
    index = Indxr("csv", "tests/test_data/sample_w_header.tsv", delimiter="\t")

    assert index.get("0") == {"id": "0", "content": "this is line 0"}
    assert index.get("1") == {"id": "1", "content": "this is line 1"}
    assert index.get("2") == {"id": "2", "content": "this is line 2"}


def test_tsv_index_wo_header():
    index = Indxr(
        "csv",
        "tests/test_data/sample_wo_header.tsv",
        fieldnames=["new_id", "content"],
        has_header=False,
        delimiter="\t",
        key_id="new_id",
    )

    assert index.get("0") == {"new_id": "0", "content": "this is line 0"}
    assert index.get("1") == {"new_id": "1", "content": "this is line 1"}
    assert index.get("2") == {"new_id": "2", "content": "this is line 2"}


def test_write_read():
    index_1 = Indxr("raw", "tests/test_data/sample.txt")
    index_1.write("tests/test_index.json")
    index_2 = Indxr.read("tests/test_index.json")

    assert index_2.kind == index_1.kind
    assert index_2.path == index_1.path
    assert index_2.kwargs == index_1.kwargs
    assert index_2.index == index_1.index

    os.remove("tests/test_index.json")
