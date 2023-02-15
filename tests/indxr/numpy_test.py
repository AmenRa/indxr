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
    data.resize((30, 40))
    fp = np.memmap(filename, dtype="float32", mode="w+", shape=(30, 40))
    fp[:] = data[:]
    fp.flush()
    return data


# TESTS ========================================================================
def test_numpy_index(filename, data):
    index = Indxr(path=filename, dtype="float32", shape=(30, 40))

    assert np.array_equal(index[0], data[0])
    assert np.array_equal(index[1], data[1])
    assert np.array_equal(index[2], data[2])


def test_numpy_get(filename, data):
    index = Indxr(path=filename, dtype="float32", shape=(30, 40))

    assert np.array_equal(index.get("0"), data[0])
    assert np.array_equal(index.get("1"), data[1])
    assert np.array_equal(index.get("2"), data[2])

    assert np.array_equal(index.get(0), data[0])
    assert np.array_equal(index.get(1), data[1])
    assert np.array_equal(index.get(2), data[2])


def test_numpy_mget(filename, data):
    index = Indxr(path=filename, dtype="float32", shape=(30, 40))

    assert np.array_equal(index.mget(["0", "1", "2"]), data[:3])
    assert np.array_equal(
        index.mget(["2", "0", "1"]), np.asarray([data[2], data[0], data[1]])
    )


def test_numpy_slice(filename, data):
    index = Indxr(path=filename, dtype="float32", shape=(30, 40))

    assert np.array_equal(index.get_slice(10, 30), data[10:30])


def test_numpy_mslice(filename, data):
    index = Indxr(path=filename, dtype="float32", shape=(30, 40))

    assert np.array_equal(
        index.mget_slice([(10, 15), (18, 27)])[0], data[10:15]
    )
    assert np.array_equal(
        index.mget_slice([(10, 15), (18, 27)])[1], data[18:27]
    )


def test_write_read(filename):
    index_1 = Indxr(path=filename, dtype="float32", shape=(30, 40))
    index_1.write("tests/test_index.json")
    index_2 = Indxr.read("tests/test_index.json")

    assert index_2.kind == index_1.kind
    assert index_2.path == index_1.path
    assert index_2.kwargs == index_1.kwargs
    assert index_2.index == index_1.index
    assert index_2.index_keys == index_1.index_keys
    assert index_2.kwargs["dtype"] == index_1.kwargs["dtype"]
    assert index_2.kwargs["shape"] == index_1.kwargs["shape"]

    os.remove("tests/test_index.json")
