import os

import pytest

from indxr import Indxr

# FIXTURES =====================================================================

# TESTS ========================================================================
def test_txt_index():
    index = Indxr("tests/test_data/sample.txt")

    assert index[0] == "this is line 0"
    assert index[1] == "this is line 1"
    assert index[2] == "this is line 2"


def test_txt_get():
    index = Indxr("tests/test_data/sample.txt")

    assert index.get("0") == "this is line 0"
    assert index.get("1") == "this is line 1"
    assert index.get("2") == "this is line 2"


def test_txt_mget():
    index = Indxr("tests/test_data/sample.txt")

    assert index.mget(["0", "1", "2"]) == [
        "this is line 0",
        "this is line 1",
        "this is line 2",
    ]
    assert index.mget(["2", "0", "1"]) == [
        "this is line 2",
        "this is line 0",
        "this is line 1",
    ]


def test_txt_callback():
    index = Indxr("tests/test_data/sample.txt", callback=lambda x: x.split())

    assert index[0] == ["this", "is", "line", "0"]
    assert index[1] == ["this", "is", "line", "1"]
    assert index[2] == ["this", "is", "line", "2"]

    assert index.get("0") == ["this", "is", "line", "0"]
    assert index.get("1") == ["this", "is", "line", "1"]
    assert index.get("2") == ["this", "is", "line", "2"]

    assert index.mget(["0", "1", "2"]) == [
        ["this", "is", "line", "0"],
        ["this", "is", "line", "1"],
        ["this", "is", "line", "2"],
    ]


def test_write_read():
    index_1 = Indxr("tests/test_data/sample.txt")
    index_1.write("tests/test_index.json")
    index_2 = Indxr.read("tests/test_index.json")

    assert index_2.kind == index_1.kind
    assert index_2.path == index_1.path
    assert index_2.kwargs == index_1.kwargs
    assert index_2.index == index_1.index
    assert index_2.index_keys == index_1.index_keys

    os.remove("tests/test_index.json")
