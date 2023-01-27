import pytest

from utils.encode_instruction import encode_instruction


@pytest.mark.parametrize("instruction, expected_output", [
    ("addi x8, x9, -12", 0xFF448413),
    ("addi x7, x0, 244", 0x0F400393),
    ("sw x2, x3, 40", 0x0221A423),
    ("lui, x5, 65535", 0x0FFFF2B7),
    ("bne x1, x2, -50", 0xFC2097E3),
    ("jal x1, -500", 0xE0DFF0EF),
    ("add x8, x9, x10", 0x00A48433),
    ("sub x1, x2, x13", 0x40D100B3),
    ("and x4, x11, x13", 0x00D5F233),
    ("slti x8, x9, 12", 0x00C4A413),
    ("xori x8, x9, 12", 0x00C4C413),
    ("sb x3, x2, -241", 0xF03107A3),
    ("sw x4, x3, 124", 0x0641AE23),
    ("sh x9, x5, 0", 0x00929023),
])
def test_encode_instruction(instruction, expected_output):
    assert encode_instruction(instruction) == expected_output