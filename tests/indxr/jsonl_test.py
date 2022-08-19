import os

import pytest

from indxr import Indxr

# FIXTURES =====================================================================

# TESTS ========================================================================
def test_jsonl_index():
    index = Indxr("tests/test_data/sample.jsonl")

    assert index[0] == {"id": "id_0", "content": "this is line 0"}
    assert index[1] == {"id": "id_1", "content": "this is line 1"}
    assert index[2] == {"id": "id_2", "content": "this is line 2"}


def test_jsonl_get():
    index = Indxr("tests/test_data/sample.jsonl")

    assert index.get("id_0") == {"id": "id_0", "content": "this is line 0"}
    assert index.get("id_1") == {"id": "id_1", "content": "this is line 1"}
    assert index.get("id_2") == {"id": "id_2", "content": "this is line 2"}


def test_jsonl_mget():
    index = Indxr("tests/test_data/sample.jsonl")

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


def test_jsonl_callback():
    index = Indxr("tests/test_data/sample.jsonl", callback=lambda x: x["id"])

    assert index[0] == "id_0"
    assert index[1] == "id_1"
    assert index[2] == "id_2"

    assert index.get("id_0") == "id_0"
    assert index.get("id_1") == "id_1"
    assert index.get("id_2") == "id_2"

    assert index.mget(["id_0", "id_1", "id_2"]) == ["id_0", "id_1", "id_2"]


def test_write_read():
    index_1 = Indxr("tests/test_data/sample.jsonl")
    index_1.write("tests/test_index.json")
    index_2 = Indxr.read("tests/test_index.json")

    assert index_2.kind == index_1.kind
    assert index_2.path == index_1.path
    assert index_2.kwargs == index_1.kwargs
    assert index_2.index == index_1.index
    assert index_2.index_keys == index_1.index_keys

    os.remove("tests/test_index.json")
