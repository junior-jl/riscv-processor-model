import pytest

from utils.encode_instruction import encode_instruction


@pytest.mark.parametrize("instruction, expected_output", [
    ("addi x8, x9, -12", 0xFF448413),
    ("addi x7, x0, 244", 0x0F400393),
    ("sw x2, x3, 40", 0x0221A423),
    ("sw x2, x3, 0x28", 0x0221A423),
    ("sw x2, x3, 0b101000", 0x0221A423),
    ("sw x2, 40(x3)", 0x0221A423),
    ("sw x2, 0x28(x3)", 0x0221A423),
    ("sw x2, 0b101000(x3)", 0x0221A423),
    ("lui, x5, 65535", 0x0FFFF2B7),
    ("lui, x5, 0xFFFF", 0x0FFFF2B7),
    ("lui, x5, 0b1111111111111111", 0x0FFFF2B7),
    ("bne x1, x2, -50", 0xFC2097E3),
    ("bne x1, x2, 0xFFFFFFCE", 0xFC2097E3),
    ("bne x1, x2, 0b111111111111111111111111111111111111111111001110", 0xFC2097E3),
    ("jal x1, -500", 0xE0DFF0EF),
    ("jal x1, 0XFFFFFE0C", 0xE0DFF0EF),
    ("jal x1, 0B111111111111111111111111111111111111111000001100", 0xE0DFF0EF),
    ("add x8, x9, x10", 0x00A48433),
    ("sub x1, x2, x13", 0x40D100B3),
    ("and x4, x11, x13", 0x00D5F233),
    ("slti x8, x9, 12", 0x00C4A413),
    ("xori x8, x9, 12", 0x00C4C413),
    ("sb x3, x2, -241", 0xF03107A3),
    ("sb x3, -241(x2)", 0xF03107A3),
    ("sw x4, x3, 124", 0x0641AE23),
    ("sw x4, 124(x3)", 0x0641AE23),
    ("sh x9, x5, 0", 0x00929023),
    ("sh x9, 0(x5)", 0x00929023),
    ("lw x3, 0(x2)", 0x00012183),
    ("lw x3, x2, 0", 0x00012183),
    ("lh x21, x7, 76", 0x04C39A83),
    ("lh x21, x7, 0x4c", 0x04C39A83),
    ("lh x21, x7, 0b1001100", 0x04C39A83),
    ("lh x21, 76(x7)", 0x04C39A83),
    ("lh x21, 0x4c(x7)", 0x04C39A83),
    ("lh x21, 0b1001100(x7)", 0x04C39A83),
])
def test_encode_instruction(instruction, expected_output):
    assert encode_instruction(instruction) == expected_output
