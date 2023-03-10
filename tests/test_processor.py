import pytest

from classes.Processor import Processor


# TODO: tests passing individually, but not together
@pytest.fixture
def cpu():
    return Processor()


def test_load_instruction_from_asm_file(cpu):
    cpu.load_instructions_from_asm_file("files/test_r.s")
    assert cpu.instructions is not None
    assert cpu.instructions == [
        1048851,
        2097555,
        52429331,
        4237296275,
        3212083,
        4293555,
        1076954163,
        1079247923,
        4388019,
        4384051,
        3216819,
        3233331,
        4376243,
        3221299,
        2205619,
        4438067,
        7485619,
        1076025651,
    ]


def test_fetch_current_instruction(cpu):
    cpu.load_instructions_from_asm_file("files/test_r.s")
    assert cpu.fetch_current_instruction() == 1048851
    cpu.datapath.prog_counter.set_value(8)
    assert cpu.fetch_current_instruction() == 52429331


def test_run_r(cpu):
    cpu.reset()
    cpu.run("files/test_r.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0
    assert cpu.datapath.reg_files.get_value(2) == 0x1
    assert cpu.datapath.reg_files.get_value(3) == 0x2
    assert cpu.datapath.reg_files.get_value(4) == 0x32
    assert cpu.datapath.reg_files.get_value(5) == 0xFFFFFFC9
    assert cpu.datapath.reg_files.get_value(6) == 0x3
    assert cpu.datapath.reg_files.get_value(7) == 0x34
    assert cpu.datapath.reg_files.get_value(8) & 0xFFFFFFFF == 0x36
    assert cpu.datapath.reg_files.get_value(9) == 0
    assert cpu.datapath.reg_files.get_value(10) == 0xFFFFFFFB
    assert cpu.datapath.reg_files.get_value(11) == 0x4
    assert cpu.datapath.reg_files.get_value(12) == 0x0
    assert cpu.datapath.reg_files.get_value(13) == 0xFFFFFFFB
    assert cpu.datapath.reg_files.get_value(14) == 0x1
    assert cpu.datapath.reg_files.get_value(15) == 0x0
    assert cpu.datapath.reg_files.get_value(16) == 0x0
    assert cpu.datapath.reg_files.get_value(17) == 0x1
    assert cpu.datapath.reg_files.get_value(18) == 0xFFFFFFE4
    x = 0
    for i in range(19, 32):
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0


def test_run_ls(cpu):
    cpu.reset()
    cpu.run("files/test_loads_stores.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0
    assert cpu.datapath.reg_files.get_value(2) == 0
    assert cpu.datapath.reg_files.get_value(3) == 0x50
    assert cpu.datapath.reg_files.get_value(4) == 0x5
    assert cpu.datapath.reg_files.get_value(5) == 0xFFFFFFEC
    assert cpu.datapath.reg_files.get_value(6) == 0x5
    assert cpu.datapath.reg_files.get_value(7) == 0xFFFFFFEC
    assert cpu.datapath.reg_files.get_value(8) == 0x5
    assert cpu.datapath.reg_files.get_value(9) == 0xFFFFFFEC
    assert cpu.datapath.reg_files.get_value(10) == 0x5
    assert cpu.datapath.reg_files.get_value(11) == 0xFFFFFFEC
    assert cpu.datapath.reg_files.get_value(12) == 0xFFEC
    assert cpu.datapath.reg_files.get_value(13) == 0xEC
    assert cpu.datapath.reg_files.get_value(20) == 0x64
    x = 0
    for i in range(14, 32):
        if i == 20:
            continue
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0
    assert cpu.datapath.data_mem.get_value(0x50) == 5
    assert cpu.datapath.data_mem.get_value(0x51) == 0
    assert cpu.datapath.data_mem.get_value(0x52) == 0
    assert cpu.datapath.data_mem.get_value(0x53) == 0
    assert cpu.datapath.data_mem.get_value(0x58) == 0xEC
    assert cpu.datapath.data_mem.get_value(0x59) == 0xFF
    assert cpu.datapath.data_mem.get_value(0x5A) == 0xFF
    assert cpu.datapath.data_mem.get_value(0x5B) == 0xFF
    assert cpu.datapath.data_mem.get_value(0x6C) == 0xEC
    assert cpu.datapath.data_mem.get_value(0x6D) == 0xFF
    assert cpu.datapath.data_mem.get_value(0x6E) == 0x00
    assert cpu.datapath.data_mem.get_value(0x6F) == 0x00


def test_run_i(cpu):
    cpu.reset()
    cpu.run("files/test_I.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0x7D0
    assert cpu.datapath.reg_files.get_value(2) == 0x1
    assert cpu.datapath.reg_files.get_value(3) == 0x2
    assert cpu.datapath.reg_files.get_value(4) == 0xFFFFFFCE
    assert cpu.datapath.reg_files.get_value(5) == 0xFFFFFFCE
    assert cpu.datapath.reg_files.get_value(6) == 0xFFFFFFFF
    assert cpu.datapath.reg_files.get_value(7) == 0x0
    assert cpu.datapath.reg_files.get_value(8) == 0x1
    assert cpu.datapath.reg_files.get_value(9) == 0x0
    assert cpu.datapath.reg_files.get_value(10) == 0x0
    assert cpu.datapath.reg_files.get_value(11) == 0x8
    assert cpu.datapath.reg_files.get_value(12) == 0xFFFFFFF3
    assert cpu.datapath.reg_files.get_value(13) == 0x1FFFFFF9
    assert cpu.datapath.reg_files.get_value(15) == 0xFFFFFFFC
    x = 0
    for i in range(14, 32):
        if i == 15:
            continue
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0


def test_run_jalr(cpu):
    cpu.reset()
    cpu.run("files/test_jalr.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0x8
    assert cpu.datapath.reg_files.get_value(2) == 0x0
    assert cpu.datapath.reg_files.get_value(3) == 0xC
    assert cpu.datapath.reg_files.get_value(7) == 0x18
    assert cpu.datapath.reg_files.get_value(31) == 0x1
    x = 0
    for i in range(4, 32):
        if i == 7 or i == 31:
            continue
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0


def test_run_uj(cpu):
    cpu.reset()
    cpu.run("files/test_uj.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0x8
    assert cpu.datapath.reg_files.get_value(2) == 0x0
    assert cpu.datapath.reg_files.get_value(3) == 0x0
    assert cpu.datapath.reg_files.get_value(4) == 0x0
    assert cpu.datapath.reg_files.get_value(5) == 0x3
    assert cpu.datapath.reg_files.get_value(6) == 0x3
    x = 0
    for i in range(7, 32):
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0


def test_run_u(cpu):
    cpu.reset()
    cpu.run("files/test_u.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0x0
    assert cpu.datapath.reg_files.get_value(2) == 0x0
    assert cpu.datapath.reg_files.get_value(3) == 0x0
    assert cpu.datapath.reg_files.get_value(4) == 0xABCDEF12
    assert cpu.datapath.reg_files.get_value(5) == 0x001F4008
    assert cpu.datapath.reg_files.get_value(6) == 0xABCDF00C
    x = 0
    for i in range(7, 32):
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0


def test_run_sb(cpu):
    cpu.reset()
    cpu.run("files/test_branches.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0x1
    assert cpu.datapath.reg_files.get_value(2) == 0x2
    assert cpu.datapath.reg_files.get_value(3) == 0xA
    assert cpu.datapath.reg_files.get_value(4) == 0x0
    assert cpu.datapath.reg_files.get_value(5) == 0x0
    assert cpu.datapath.reg_files.get_value(6) == 0x28
    assert cpu.datapath.reg_files.get_value(7) == 0x0
    assert cpu.datapath.reg_files.get_value(8) == 0x3C
    x = 0
    for i in range(9, 32):
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0


def test_run_general_1(cpu):
    cpu.reset()
    cpu.run("files/general_test_1.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0x0
    assert cpu.datapath.reg_files.get_value(2) == 0x0
    assert cpu.datapath.reg_files.get_value(3) == 0x0
    assert cpu.datapath.reg_files.get_value(4) == 0x0
    assert cpu.datapath.reg_files.get_value(5) == 0x0
    assert cpu.datapath.reg_files.get_value(6) == 0x28
    assert cpu.datapath.reg_files.get_value(7) == 0x0
    assert cpu.datapath.reg_files.get_value(8) == 0x3C
    assert cpu.datapath.reg_files.get_value(10) == 0x1
    assert cpu.datapath.reg_files.get_value(15) == 0xC
    assert cpu.datapath.reg_files.get_value(20) == 0x2
    x = 0
    for i in range(9, 32):
        if i in [10, 15, 20]:
            continue
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0

def test_run_general_2(cpu):
    cpu.reset()
    cpu.run("files/book_test.s")
    assert cpu.datapath.reg_files.get_value(0) == 0
    assert cpu.datapath.reg_files.get_value(1) == 0x0
    assert cpu.datapath.reg_files.get_value(2) == 0x19
    assert cpu.datapath.reg_files.get_value(3) == 0x44
    assert cpu.datapath.reg_files.get_value(4) == 0x1
    assert cpu.datapath.reg_files.get_value(5) == 0xB
    assert cpu.datapath.reg_files.get_value(6) == 0x0
    assert cpu.datapath.reg_files.get_value(7) == 0x7
    assert cpu.datapath.reg_files.get_value(8) == 0x0
    assert cpu.datapath.reg_files.get_value(9) == 0x12
    assert cpu.datapath.data_mem.get_value(100) == 0x19
    assert cpu.datapath.data_mem.get_value(96) == 0x7
    x = 0
    for i in range(10, 32):
        x |= cpu.datapath.reg_files.get_value(i)
    assert x == 0
