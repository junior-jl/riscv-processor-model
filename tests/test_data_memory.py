import pytest

from classes.DataMemory import DataMemory
from utils.sign_extend import sign_extend


def test_init():
    dm = DataMemory(16)
    assert dm.words == 16
    assert dm.data == [0] * 64
    assert dm.data_in is None
    assert dm.data_out is None
    assert not dm.write_enable
    assert not dm.read_enable


def test_get_value():
    dm = DataMemory(16)
    dm.data[0] = 5
    assert dm.get_value(0) == 5


def test_set_enable():
    dm = DataMemory(16)
    dm.set_enable(False, False)
    assert not dm.write_enable
    assert not dm.read_enable
    dm.set_enable(True, True)
    assert dm.write_enable
    assert dm.read_enable


def test_load():
    dm = DataMemory(16)
    dm.data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    dm.set_enable(False, True)
    assert dm.load(0, DataMemory.WORD, False) == 0x04030201
    assert dm.load(4, DataMemory.HALF_WORD, False) == 0x0605
    assert dm.load(8, DataMemory.BYTE, False) == 0x09
    dm.set_enable(False, False)
    assert dm.load(0, DataMemory.WORD, False) == "Read Enable is unset!"
    dm.set_enable(False, True)
    with pytest.raises(ValueError):
        dm.load(0, 5, False)
    with pytest.raises(IndexError):
        dm.load(100, DataMemory.WORD, False)


def test_store():
    dm = DataMemory(16)
    dm.set_enable(True, False)
    assert dm.store(0, 0x04030201, DataMemory.WORD) == 0x04030201
    assert dm.data[0:4] == [1, 2, 3, 4]
    assert dm.store(4, 0x0605, DataMemory.HALF_WORD) == 0x0605
    assert dm.data[4:6] == [5, 6]
    assert dm.store(8, 0x07, DataMemory.BYTE) == 0x07
    assert dm.data[8] == 0x07
    dm.set_enable(False, False)
    assert dm.store(0, 0x04030201, DataMemory.WORD) == "Write Enable is unset!"
    dm.set_enable(True, False)
    with pytest.raises(ValueError):
        dm.store(0, 0x04030201, 5)
    with pytest.raises(IndexError):
        dm.store(100, 5, DataMemory.WORD)
