import pytest

from classes.Processor import Processor


@pytest.fixture
def cpu():
    return Processor()


# 1048851
# 2097555
# 52429331
# 4503599626322579
# 3212083
# 4293555
# 1076954163
# 1079247923
# 4388019
# 4384051
# 3216819
# 3233331
# 4376243
# 3221299
# 2205619
# 4438067
# 7485619
# 1076025651

def test_load_instruction_from_asm_file(cpu):
    cpu.load_instructions_from_asm_file('files/teste_r.s')
    assert cpu.instructions is not None
    assert cpu.instructions == [1048851,
                                2097555,
                                52429331,
                                -57671021,
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
                                1076025651]


def test_fetch_current_instruction(cpu):
    cpu.load_instructions_from_asm_file('files/teste_r.s')
    assert cpu.fetch_current_instruction() == 1048851
    cpu.datapath.prog_counter.set_value(8)
    assert cpu.fetch_current_instruction() == 52429331


def test_run(cpu):
    cpu.run('files/teste_r.s')
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