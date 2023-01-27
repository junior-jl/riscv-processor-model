from classes.ALU import ALU
from classes.ControlUnit import ControlUnit
from classes.DataMemory import DataMemory
from classes.Datapath import Datapath
from classes.InstructionMemory import InstructionMemory
from classes.ProgramCounter import ProgramCounter
from classes.RegisterFiles import RegisterFiles
from utils.encode_instruction import encode_instruction
from utils.encode_instructions import encode_instructions_from_file, print_encoded_instructions


# 1. Instruction Fetch
# 2. Instruction Decode
# 3. Execute
# 4. Memory
# 5. Write Back

def fetch_current_instruction(inst_mem: InstructionMemory, pc):
    return inst_mem.fetch_instruction(pc)


# TODO: Accept format with parenthesis
if __name__ == '__main__':
    im = InstructionMemory(32)
    pc = ProgramCounter()
    rf = RegisterFiles(32)
    alu = ALU()
    dm = DataMemory(32)
    dp = Datapath(im, pc, rf, alu, dm)
    ctrl = ControlUnit
    code = encode_instructions_from_file('classes/teste.s')
    im.fill_memory(code)
    im.print_instructions()
    print(fetch_current_instruction(im, pc.value))
