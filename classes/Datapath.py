from classes.ALU import ALU
from classes.BranchComparator import BranchComparator
from classes.DataMemory import DataMemory
from classes.ImmediateGenerator import ImmediateGenerator
from classes.InstructionMemory import InstructionMemory
from classes.ProgramCounter import ProgramCounter
from classes.RegisterFiles import RegisterFiles
from utils.mask_bits import mask_bits


# 1. Instruction Fetch
# 2. Instruction Decode
# 3. Execute
# 4. Memory
# 5. Write Back

class Datapath():
    """
    The Datapath class represents the data path of a RISC-V processor model. It contains all the components of the
    data path such as the instruction memory, program counter, register files, ALU, data memory, branch comparator
    and immediate generator.
    """

    def __init__(self, inst_mem: InstructionMemory = InstructionMemory(),
                 prog_counter: ProgramCounter = ProgramCounter(),
                 reg_files: RegisterFiles = RegisterFiles(),
                 alu: ALU = ALU(),
                 data_mem: DataMemory = DataMemory(),
                 branch_comparator: BranchComparator = BranchComparator(),
                 immediate_generator: ImmediateGenerator = ImmediateGenerator()):
        """
        Initialize the components of the datapath.

        :param inst_mem: An instance of the InstructionMemory class
        :param prog_counter: An instance of the ProgramCounter class
        :param reg_files: An instance of the RegisterFiles class
        :param alu: An instance of the ALU class
        :param data_mem: An instance of the DataMemory class
        :param branch_comparator: An instance of the BranchComparator class
        :param immediate_generator: An instance of the ImmediateGenerator class
        """
        self.reg_w_en = None
        self.inst_mem = inst_mem
        self.prog_counter = prog_counter
        self.reg_files = reg_files
        self.alu = alu
        self.data_mem = data_mem
        self.branch_comparator = branch_comparator
        self.immediate_generator = immediate_generator
        self.current_instruction = None
        self.mem_rw = None
        self.pc_sel = 0
        self.wb_sel = 0

    def fetch_current_instruction(self):
        """
        Fetch the current instruction from the instruction memory at the current program counter value.

        :return: The current instruction
        """
        self.current_instruction = self.inst_mem.fetch_instruction(self.prog_counter.get_value())
        return self.current_instruction

    def get_pc(self):
        """
        Get the current value of the program counter.

        :return: The current program counter value
        """
        return self.prog_counter.get_value()

    def set_pc_sel(self, sel):
        """
        Set the selection of the program counter update.

        :param sel: 1 for ALU output and 0 for PC increment
        """
        self.pc_sel = sel

    def update_pc(self):
        """
        Update the program counter according to the current selection.
        """
        if self.pc_sel:
            self.prog_counter.offset(self.get_alu_output())  # alu_out
        else:
            self.increment_pc()

    def get_alu_output(self):
        """
        Get the output of the ALU.

        :return: The output of the ALU
        """
        return self.alu.get_output()

    def get_immediate(self):
        """
        Get the current immediate value.

        :return: The current immediate value
        """
        return self.immediate_generator.get_immediate()

    def increment_pc(self):
        """
        Increment the program counter by 4 (1 instruction).
        """
        self.prog_counter.increment()

    def split_instruction(self):
        """
        Split the current instruction into its components and pass them to the corresponding components.

        :return: The destination register address, source register 1 address, source register 2 address and immediate
        value
        """
        rs1 = mask_bits(self.current_instruction, 15, 19)
        rs2 = mask_bits(self.current_instruction, 20, 24)
        rd = mask_bits(self.current_instruction, 7, 11)
        self.reg_files.set_addresses(rd, rs1, rs2)
        imm = mask_bits(self.current_instruction, 7, 31)
        self.immediate_generator.pass_immediate(imm)
        return rd, rs1, rs2, imm

    def get_value_rs1(self):
        """
        Get the value of source register 1.

        :return: The value of source register 1
        """
        return self.reg_files.get_value_rs1()

    def get_value_rs2(self):
        """
        Get the value of source register 2.

        :return: The value of source register 2
        """
        return self.reg_files.get_value_rs2()

    def get_value_rd(self):
        """
        Get the value of destination register.

        :return: The value of destination register
        """
        return self.reg_files.get_value_rd()

    def set_reg_w_en(self, enable):

        self.reg_w_en = enable
        self.reg_files.set_write_enable(self.reg_w_en)

    def compare(self, uns):
        data_rs1 = self.get_value_rs1()
        data_rs2 = self.get_value_rs2()
        self.branch_comparator.pass_inputs(data_rs1, data_rs2)
        if uns:
            self.branch_comparator.set_unsigned()
        self.branch_comparator.compare()

    def pass_alu_inputs(self, a_sel, b_sel):
        a = self.get_pc() if a_sel else self.get_value_rs1()
        b = self.get_immediate() if b_sel else self.get_value_rs2()
        self.alu.pass_inputs(a, b)

    def set_alu_operation(self, operation):
        self.alu.set_select(operation)

    def operate(self):
        return self.alu.operate()

    # mem_rw 0 read 1 write
    def set_mem_rw(self, mem_rw):
        self.data_mem.set_enable(write=mem_rw, read=not mem_rw)

    def set_imm_sel(self, imm_sel):
        self.immediate_generator.set_selection(imm_sel)

    def load_from_memory(self, size):
        address = self.operate()
        value = self.data_mem.load(address, size)
        self.reg_files.write(value)
        return value

    def load_from_alu(self):
        self.reg_files.write(self.operate())

    def load_from_pc(self):
        self.reg_files.write(self.get_pc() + 4)

    def store_into_memory(self, size):
        address = self.operate()
        value = self.get_value_rs2()
        return self.data_mem.store(address, value, size)

    def set_wb_sel(self, value):
        self.wb_sel = value

    def write_back(self, size):
        if self.wb_sel == 0:
            return self.load_from_memory(size)
        elif self.wb_sel == 1:
            return self.load_from_alu()
        elif self.wb_sel == 2:
            return self.load_from_pc()
        else:
            raise ValueError('Invalid option for WBSel!')

    def load_instructions_from_file(self, file):
        self.inst_mem.load_instructions_from_file(file)

    def load_instructions_from_asm_file(self, file):
        self.inst_mem.load_instructions_from_asm_file(file)

    def print_registers(self):
        self.reg_files.print_all()

    def print_data_memory(self):
        self.data_mem.print_data()

    def print_instructions(self):
        self.inst_mem.print_instructions()
