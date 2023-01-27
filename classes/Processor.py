from classes.ALU import ALU
from classes.DataMemory import DataMemory
from classes.Datapath import Datapath
from classes.ControlUnit import ControlUnit
from classes.InstructionMemory import InstructionMemory
from classes.ProgramCounter import ProgramCounter
from classes.RegisterFiles import RegisterFiles
from utils.encode_instructions import encode_instructions_from_file

# 1. Instruction Fetch
# 2. Instruction Decode
# 3. Execute
# 4. Memory
# 5. Write Back

class Processor:
    def __init__(self, datapath: Datapath, control: ControlUnit):
        self.datapath = datapath
        self.control = control

    def fetch_current_instruction(self):
        pass


im = InstructionMemory(32)
pc = ProgramCounter()
rf = RegisterFiles(32)
alu = ALU()
dm = DataMemory(32)
dp = Datapath(im, pc, rf, alu, dm)
ctrl = ControlUnit
code = encode_instructions_from_file('teste.s')
im.fill_memory(code)
im.print_instructions()
cpu = Processor(dp, ctrl)

