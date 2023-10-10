import os
import os.path as path

import numpy as np
import pytest

from indxr import Indxr


# FIXTURES =====================================================================
@pytest.fixture
def filename():
    return path.join("tests/test_data", "sample.dat")


@pytest.fixture
def data(filename):
    data = np.arange(120, dtype=np.float32)
    data = np.resize(data, (30, 40))
    fp = np.memmap(filename, dtype="float32", mode="w+", shape=(30, 40))
    fp[:] = data[:]
    fp.flush()
    return data


@pytest.fixture
def mapping():
    return {
        "doc_1": {
            "offset": 0,
            "length": 6,
        },
        "doc_2": {
            "offset": 6,
            "length": 10,
        },
        "doc_3": {
            "offset": 16,
            "length": 14,
        },
    }


# TESTS ========================================================================
def test_numpy_get(filename, data, mapping):
    index = Indxr(path=filename, dtype="float32", shape=(30, 40), mapping=mapping)

    assert np.array_equal(index.get("doc_1"), data[0:6])
    assert np.array_equal(index.get("doc_2"), data[6:16])
    assert np.array_equal(index.get("doc_3"), data[16:30])


def test_numpy_mget(filename, data, mapping):
    index = Indxr(path=filename, dtype="float32", shape=(30, 40), mapping=mapping)

    out = index.mget(["doc_1", "doc_2", "doc_3"])

    assert np.array_equal(out[0], data[0:6])
    assert np.array_equal(out[1], data[6:16])
    assert np.array_equal(out[2], data[16:30])

    out = index.mget(["doc_3", "doc_1", "doc_2"])

    assert np.array_equal(out[0], data[16:30])
    assert np.array_equal(out[1], data[0:6])
    assert np.array_equal(out[2], data[6:16])


def test_write_read(filename, data, mapping):
    index_1 = Indxr(path=filename, dtype="float32", shape=(30, 40), mapping=mapping)
    index_1.write("tests/test_index.json")
    index_2 = Indxr.read("tests/test_index.json")

    assert index_2.kind == index_1.kind
    assert index_2.path == index_1.path
    assert index_2.kwargs == index_1.kwargs
    assert index_2.index == index_1.index
    assert index_2.index_keys == index_1.index_keys
    assert index_2.kwargs["dtype"] == index_1.kwargs["dtype"]
    assert index_2.kwargs["shape"] == index_1.kwargs["shape"]

    assert np.array_equal(index_2.get("doc_1"), data[0:6])
    assert np.array_equal(index_2.get("doc_2"), data[6:16])
    assert np.array_equal(index_2.get("doc_3"), data[16:30])

    os.remove("tests/test_index.json")
