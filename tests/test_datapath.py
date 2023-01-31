import pytest

from classes.ALU import ALU
from classes.BranchComparator import BranchComparator
from classes.DataMemory import DataMemory
from classes.Datapath import Datapath
from classes.ImmediateGenerator import ImmediateGenerator
from classes.InstructionMemory import InstructionMemory
from classes.InstructionType import InstructionType
from classes.ProgramCounter import ProgramCounter
from classes.RegisterFiles import RegisterFiles


@pytest.fixture
def datapath():
    inst_mem = InstructionMemory(32)
    prog_counter = ProgramCounter()
    reg_files = RegisterFiles(32)
    alu = ALU()
    data_mem = DataMemory(32)
    branch_comparator = BranchComparator()
    immediate_generator = ImmediateGenerator()
    return Datapath(inst_mem, prog_counter, reg_files, alu, data_mem, branch_comparator, immediate_generator)


def test_fetch_current_instruction(datapath):
    inst = 0x12345678
    datapath.inst_mem.instructions = [inst, 3, 4]
    datapath.prog_counter.set_value(0)
    assert datapath.fetch_current_instruction() == inst
    datapath.prog_counter.set_value(8)
    assert datapath.fetch_current_instruction() == 4


def test_get_pc(datapath):
    datapath.prog_counter.set_value(100)
    assert datapath.get_pc() == 100


def test_set_pc_sel(datapath):
    datapath.set_pc_sel(1)
    assert datapath.pc_sel == 1


def test_update_pc(datapath):
    datapath.prog_counter.set_value(100)
    datapath.set_pc_sel(1)
    datapath.alu.output = 200
    datapath.update_pc()
    assert datapath.prog_counter.get_value() == 300


def test_increment_pc(datapath):
    datapath.prog_counter.set_value(100)
    datapath.increment_pc()
    assert datapath.prog_counter.get_value() == 104


def test_split_instruction(datapath):
    datapath.current_instruction = 0x12345678
    rd, rs1, rs2, imm = datapath.split_instruction()
    assert rd == 0xC
    assert rs1 == 0x8
    assert rs2 == 0x3
    assert imm == 0x02468AC


def test_get_value_rs1(datapath):
    datapath.reg_files.set_addresses(1, 2, 3)
    assert datapath.reg_files.get_value_rs1() == 0
    datapath.reg_files.set_write_enable(True)
    datapath.reg_files.write(7)
    datapath.reg_files.set_addresses(2, 1, 3)
    assert datapath.reg_files.get_value_rs1() == 7
    assert datapath.reg_files.get_value(1) == 7


def test_get_value_rs2(datapath):
    datapath.reg_files.set_addresses(1, 2, 3)
    assert datapath.reg_files.get_value_rs2() == 0
    datapath.reg_files.set_write_enable(True)
    datapath.reg_files.write(7)
    datapath.reg_files.set_addresses(3, 7, 1)
    assert datapath.reg_files.get_value_rs2() == 7
    assert datapath.reg_files.get_value(1) == 7


def test_get_immediate(datapath):
    datapath.immediate_generator.imm_in = 0x1579BDE  # (1 0101 0111 1001 1011 1101 1110)
    datapath.immediate_generator.set_selection('I')
    assert datapath.get_immediate() == 0xFFFFFABC  # (ABC) sign-extended


def test_get_value_rd(datapath):
    datapath.reg_files.set_addresses(1, 2, 3)
    assert datapath.reg_files.get_value_rd() == 0
    datapath.reg_files.set_write_enable(True)
    datapath.reg_files.write(7)
    assert datapath.reg_files.get_value_rd() == 7
    datapath.reg_files.write(0xCC)
    assert datapath.reg_files.get_value_rd() == 0xCC


def test_set_reg_w_en(datapath):
    datapath.set_signals(0, 0, 0, 0, 0, 'add', InstructionType.I, 0, 1, 2, 0)
    assert datapath.reg_w_en == 1
