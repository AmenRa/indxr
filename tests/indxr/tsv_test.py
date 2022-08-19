import os

import pytest

from indxr import Indxr

# FIXTURES =====================================================================

# TESTS ========================================================================
def test_tsv_index_w_header():
    index = Indxr("tests/test_data/sample_w_header.tsv")

    assert index[0] == {"id": "0", "content": "this is line 0"}
    assert index[1] == {"id": "1", "content": "this is line 1"}
    assert index[2] == {"id": "2", "content": "this is line 2"}


def test_tsv_index_wo_header():
    index = Indxr(
        "tests/test_data/sample_wo_header.tsv",
        fieldnames=["new_id", "content"],
        has_header=False,
        key_id="new_id",
    )

    assert index[0] == {"new_id": "0", "content": "this is line 0"}
    assert index[1] == {"new_id": "1", "content": "this is line 1"}
    assert index[2] == {"new_id": "2", "content": "this is line 2"}


def test_tsv_get():
    index = Indxr("tests/test_data/sample_w_header.tsv")

    assert index.get("0") == {"id": "0", "content": "this is line 0"}
    assert index.get("1") == {"id": "1", "content": "this is line 1"}
    assert index.get("2") == {"id": "2", "content": "this is line 2"}


def test_tsv_mget():
    index = Indxr("tests/test_data/sample_w_header.tsv")

    assert index.mget(["0", "1", "2"]) == [
        {"id": "0", "content": "this is line 0"},
        {"id": "1", "content": "this is line 1"},
        {"id": "2", "content": "this is line 2"},
    ]
    assert index.mget(["2", "0", "1"]) == [
        {"id": "2", "content": "this is line 2"},
        {"id": "0", "content": "this is line 0"},
        {"id": "1", "content": "this is line 1"},
    ]


def test_tsv_callback():
    index = Indxr(
        "tests/test_data/sample_w_header.tsv", callback=lambda x: x["id"]
    )

    assert index[0] == "0"
    assert index[1] == "1"
    assert index[2] == "2"

    assert index.get("0") == "0"
    assert index.get("1") == "1"
    assert index.get("2") == "2"

    assert index.mget(["0", "1", "2"]) == ["0", "1", "2"]


def test_write_read():
    index_1 = Indxr("tests/test_data/sample_w_header.tsv")
    index_1.write("tests/test_index.json")
    index_2 = Indxr.read("tests/test_index.json")

    assert index_2.kind == index_1.kind
    assert index_2.path == index_1.path
    assert index_2.kwargs == index_1.kwargs
    assert index_2.index == index_1.index
    assert index_2.index_keys == index_1.index_keys

    os.remove("tests/test_index.json")
