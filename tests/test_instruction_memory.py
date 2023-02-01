import pytest

from classes.InstructionMemory import InstructionMemory


def test_init():
    im = InstructionMemory(16)
    assert len(im.instructions) == 16
    assert all(val == 0 for val in im.instructions)
    im = InstructionMemory(16, [1, 2, 3, 4])
    assert len(im.instructions) == 4
    assert im.instructions == [1, 2, 3, 4]


def test_fetch_instruction():
    im = InstructionMemory(16, list(range(16)))
    assert im.fetch_instruction(0) == 0
    assert im.fetch_instruction(4) == 1
    with pytest.raises(ValueError):
        im.fetch_instruction(3)
    with pytest.raises(IndexError):
        im.fetch_instruction(64)


def test_fill_memory():
    im = InstructionMemory(8)
    im.fill_memory([1, 2, 3, 4])
    assert im.instructions == [1, 2, 3, 4, 0, 0, 0, 0]
    im.fill_memory([5, 6, 7])
    assert im.instructions[:4] == [5, 6, 7, 4]


def test_load_instructions_from_file(tmpdir):
    # Create a temporary file with the string "12345678"
    temp_file = tmpdir.mkdir("sub").join("test.txt")
    temp_file.write("1234")

    mem = InstructionMemory(4)
    mem.load_instructions_from_file(temp_file.strpath)
    assert mem.instructions == [1234, 0, 0, 0]


def test_extend_memory():
    im = InstructionMemory(16)
    im.extend_memory(8)
    assert len(im.instructions) == 24
    assert all(val == 0 for val in im.instructions[16:])


def test_fill_memory_bytes():
    # Test case 1: Check that the function correctly splits an instruction into 4 bytes
    im = InstructionMemory(4, [0x01234567])
    expected_bytes = [0x67, 0x45, 0x23, 0x01]
    assert im.instructions_bytes == expected_bytes

    # Test case 2: Check that the function correctly splits multiple instructions into bytes
    im = InstructionMemory(8, [0x01234567, 0x89ABCDEF])
    expected_bytes = [0x67, 0x45, 0x23, 0x01, 0xEF, 0xCD, 0xAB, 0x89]
    assert im.instructions_bytes == expected_bytes

    # Test case 3: Check that the function handles empty input correctly
    im = InstructionMemory(0, [])
    assert im.instructions_bytes == []
