import os

import pytest

from indxr import Indxr

# FIXTURES =====================================================================

# TESTS ========================================================================
def test_custom_index():
    index = Indxr("tests/test_data/sample.txt", kind="custom")

    assert index[0] == b"this is line 0"
    assert index[1] == b"this is line 1"
    assert index[2] == b"this is line 2"


def test_custom_get():
    index = Indxr("tests/test_data/sample.txt", kind="custom")

    assert index.get("0") == b"this is line 0"
    assert index.get("1") == b"this is line 1"
    assert index.get("2") == b"this is line 2"


def test_custom_mget():
    index = Indxr("tests/test_data/sample.txt", kind="custom")

    assert index.mget(["0", "1", "2"]) == [
        b"this is line 0",
        b"this is line 1",
        b"this is line 2",
    ]
    assert index.mget(["2", "0", "1"]) == [
        b"this is line 2",
        b"this is line 0",
        b"this is line 1",
    ]


def test_custom_callback():
    index = Indxr(
        "tests/test_data/sample.txt",
        callback=lambda x: x.decode().split(),
        kind="custom",
    )

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
    index_1 = Indxr("tests/test_data/sample.txt", kind="custom")
    index_1.write("tests/test_index.json")
    index_2 = Indxr.read("tests/test_index.json")

    assert index_2.kind == index_1.kind
    assert index_2.path == index_1.path
    assert index_2.kwargs == index_1.kwargs
    assert index_2.index == index_1.index
    assert index_2.index_keys == index_1.index_keys

    os.remove("tests/test_index.json")
