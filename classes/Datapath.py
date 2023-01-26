from classes.ALU import ALU
from classes.InstructionMemory import InstructionMemory
from classes.ProgramCounter import ProgramCounter
from classes.RegisterFiles import RegisterFiles


class Datapath:
    def __init__(self, inst_mem, prog_counter, reg_files, alu):
        self.inst_mem = inst_mem
        self.prog_counter = prog_counter
        self.reg_files = reg_files
        self.alu = alu


im = InstructionMemory(32)
pc = ProgramCounter()
rf = RegisterFiles(32)
alu = ALU()
dp = Datapath(im, pc, rf, alu)
