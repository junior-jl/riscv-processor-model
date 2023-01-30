from classes.Datapath import Datapath
from classes.ControlUnit import ControlUnit

from utils.encode_instructions import encode_instructions_from_file


# 1. Instruction Fetch
# 2. Instruction Decode
# 3. Execute
# 4. Memory
# 5. Write Back

class Processor:
    def __init__(self, datapath: Datapath = Datapath(), control: ControlUnit = ControlUnit()):
        self.datapath = datapath
        self.control = control
        self.instructions = None
        self.current_instruction = None

    def load_instructions_from_file(self, file):
        self.datapath.load_instructions_from_file(file)

    def load_instructions_from_asm_file(self, file):
        self.instructions = self.datapath.load_instructions_from_asm_file(file)

    def fetch_current_instruction(self):
        self.current_instruction = self.datapath.fetch_current_instruction()
        self.control.fetch_instruction(self.current_instruction)
        return self.current_instruction

    def set_control_signals(self):
        self.control.set_signals()

    def print_registers(self):
        self.datapath.print_registers()

    def print_data_memory(self):
        self.datapath.print_data_memory()

    def print_instructions(self):
        self.datapath.print_instructions()

    def run(self, file):
        self.load_instructions_from_asm_file(file)
        for i in range(len(self.instructions)):
            print(f'Instruction {i + 1}:  {self.fetch_current_instruction()}')
            self.fetch_current_instruction()
            self.control.run()
            self.datapath.set_signals(*self.control.get_signals())
            self.datapath.run()
            self.print_registers()

        self.print_data_memory()



