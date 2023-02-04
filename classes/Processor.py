from classes.Datapath import Datapath
from classes.ControlUnit import ControlUnit

from utils.encode_instructions import encode_instructions_from_file


# 1. Instruction Fetch
# 2. Instruction Decode
# 3. Execute
# 4. Memory
# 5. Write Back


class Processor:
    """
    The Processor class models a RISC-V Single Cycle Processor containing a datapath and a control unit. The datapath
    is equipped with the following blocks: ALU, branch comparator, data memory, immediate generator, instruction
    memory, program counter, register files.
    """

    def __init__(
        self, datapath: Datapath = Datapath(), control: ControlUnit = ControlUnit()
    ):
        """
        Constructor method
        :param datapath: the datapath of the processor
        :type datapath: Datapath
        :param control: the control unit of the processor
        :type control: ControlUnit
        """
        self.datapath = datapath
        self.control = control
        self.instructions = None
        self.current_instruction = None

    def load_instructions_from_file(self, file):
        """
        Load instructions from binary file into the instruction memory.
        :param file: binary file containing instructions
        :type file: file
        :return: None
        :rtype: NoneType
        """
        self.datapath.load_instructions_from_file(file)

    def load_instructions_from_asm_file(self, file):
        """
        Load instructions from RISC-V Assembly file into the instruction memory.
        :param file: asm file containing instructions
        :type file: file
        :return: list of instructions
        :rtype: list
        """
        self.instructions = self.datapath.load_instructions_from_asm_file(file)

    def fetch_current_instruction(self):
        """
        Fetch the current instruction pointed by the program counter.

        :return: the current instruction
        :rtype: int
        """
        self.current_instruction = self.datapath.fetch_current_instruction()
        self.control.fetch_instruction(self.current_instruction)
        return self.current_instruction

    def set_control_signals(self):
        """
        Sets the signals in the control unit based on the current instruction.

        :return: None
        :rtype: NoneType
        """
        self.control.set_signals()

    def print_registers(self):
        """
        Prints the content of all the registers.

        :return: None
        :rtype: NoneType
        """
        self.datapath.print_registers()

    def print_data_memory(self):
        """
        Prints the content of data memory.

        :return: None
        :rtype: NoneType
        """
        self.datapath.print_data_memory()

    def print_instructions(self):
        """
        Prints the content of instruction memory.

        :return: None
        :rtype: NoneType
        """
        self.datapath.print_instructions()

    def run(self, file):
        """
        Performs the actions of the Processor.
            1. Instruction Fetch
            2. Instruction Decode
            3. Execute
            4. Memory
            5. Write Back
        The auxiliary method is different if the instruction is a branch.

        :param file: file with the instructions
        :type file: file
        :return: None
        :rtype: NoneType
        """
        self.load_instructions_from_asm_file(file)
        while self.fetch_current_instruction():
            if self.current_instruction & 0x7F == 0x63:
                self.run_branch()
            else:
                self.run_regular()

    def run_regular(self):
        """
        Performs operation of the processor based on the instruction if it is not a branch.

        :return: None
        :rtype: NoneType
        """
        # print(
        #    "IMEM {:0X}:  {:08X}".format(
        #        4 * self.instructions.index(self.current_instruction),
        #        self.current_instruction,
        #    )
        # )
        self.control.run()
        self.datapath.set_signals(*self.control.get_signals())
        self.datapath.run()
        # self.print_registers()
        # self.print_data_memory()

    def run_branch(self):
        """
        Performs the operations of the processor with the corrected flow in a branch instruction.

        :return: None
        :rtype: NoneType
        """
        # print(
        #    "IMEM {:0X}:  {:08X}".format(
        #        4 * self.instructions.index(self.current_instruction),
        #        self.current_instruction,
        #    )
        # )
        self.control.run()
        self.datapath.set_signals(*self.control.get_signals())
        self.datapath.first_run_branch()
        self.control.branch(self.datapath.branch_eq, self.datapath.branch_lt)
        self.control.set_pc_sel()
        self.datapath.set_pc_sel(self.control.pc_sel)
        self.datapath.second_run_branch()
        # self.print_registers()

    def reset(self):
        """
        Resets the processor.

        :return: None
        :rtype: NoneType
        """
        self.datapath = Datapath()
        self.datapath.reset()
        self.control = ControlUnit()
        self.control.reset()
        self.instructions = None
        self.current_instruction = None

    def print_reg(self, key):
        """
        Prints a register in the Register Files given a key.
        :param key: the register to print
        :type key: int
        :return: None
        :rtype: NoneType
        """
        print(f"Register {key}: {self.datapath.reg_files.get_value(key)}")

    def print_data_address(self, address):
        """
        Prints a value in the memory data given an address.
        :param address: the address to the data memory
        :type address: int
        :return: None
        :rtype: NoneType
        """
        self.datapath.data_mem.print_address(address)
