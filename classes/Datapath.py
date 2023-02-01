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


class Datapath:
    """
    The Datapath class represents the data path of a RISC-V processor model. It contains all the components of the
    data path such as the instruction memory, program counter, register files, ALU, data memory, branch comparator
    and immediate generator.
    """

    def __init__(
        self,
        inst_mem: InstructionMemory = InstructionMemory(),
        prog_counter: ProgramCounter = ProgramCounter(),
        reg_files: RegisterFiles = RegisterFiles(),
        alu: ALU = ALU(),
        data_mem: DataMemory = DataMemory(),
        branch_comparator: BranchComparator = BranchComparator(),
        immediate_generator: ImmediateGenerator = ImmediateGenerator(),
    ):
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
        self.imm_sel = None
        self.branch_unsigned = False
        self.branch_eq = False
        self.branch_lt = False
        self.a_sel = None
        self.b_sel = None
        self.alu_sel = None
        self.store_size = None
        self.load_size = None
        self.load_unsigned = False

    def reset(self):
        """
        Resets the datapath signals.
        TODO: update constructor method to use this method instead of repetition.

        :return: None
        :rtype: NoneType
        """
        self.reg_w_en = None
        self.inst_mem = InstructionMemory()
        self.prog_counter = ProgramCounter()
        self.reg_files = RegisterFiles()
        self.alu = ALU()
        self.data_mem = DataMemory()
        self.branch_comparator = BranchComparator()
        self.immediate_generator = ImmediateGenerator()
        self.current_instruction = None
        self.mem_rw = None
        self.pc_sel = 0
        self.wb_sel = 0
        self.imm_sel = None
        self.branch_unsigned = False
        self.branch_eq = False
        self.branch_lt = False
        self.a_sel = None
        self.b_sel = None
        self.alu_sel = None
        self.store_size = None
        self.load_size = None
        self.load_unsigned = False

    def run(self):
        """
        Runs datapath to perform the current instruction.

        :return: None
        :rtype: NoneType
        """
        self.fetch_current_instruction()
        self.split_instruction()
        self.set_reg_w_en(self.reg_w_en)
        self.compare(self.branch_unsigned)
        self.set_imm_sel(self.imm_sel)
        self.pass_alu_inputs(self.a_sel, self.b_sel)
        self.set_alu_operation(self.alu_sel)
        self.operate()
        self.set_mem_rw(self.mem_rw)
        self.store_into_memory(self.store_size)
        self.set_wb_sel(self.wb_sel)
        self.write_back(self.load_size, self.load_unsigned)
        self.set_pc_sel(self.pc_sel)
        self.update_pc()

    def first_run_branch(self):
        """
        Runs the first part of operation in branch instructions.

        :return: None
        :rtype: NoneType
        """
        self.fetch_current_instruction()
        self.split_instruction()
        self.set_reg_w_en(self.reg_w_en)
        self.compare(self.branch_unsigned)

    def second_run_branch(self):
        """
        Runs the second part of operation in branch instructions (after passing to the control unit the result of the
        comparison)

        :return: None
        :rtype: NoneType
        """
        self.set_imm_sel(self.imm_sel)
        self.pass_alu_inputs(self.a_sel, self.b_sel)
        self.set_alu_operation(self.alu_sel)
        self.operate()
        self.set_mem_rw(self.mem_rw)
        self.store_into_memory(self.store_size)
        self.set_wb_sel(self.wb_sel)
        self.write_back(self.load_size, self.load_unsigned)
        self.set_pc_sel(self.pc_sel)
        self.update_pc()

    def fetch_current_instruction(self):
        """
        Fetch the current instruction from the instruction memory at the current program counter value.

        :return: The current instruction
        :rtype: int
        """
        self.current_instruction = self.inst_mem.fetch_instruction(
            self.prog_counter.get_value()
        )
        return self.current_instruction

    def get_pc(self):
        """
        Get the current value of the program counter.

        :return: The current program counter value
        :rtype: int
        """
        return self.prog_counter.get_value()

    def set_pc_sel(self, sel):
        """
        Set the selection of the program counter update.

        :param sel: 1 for ALU output and 0 for PC increment
        :type sel: int
        :return: None
        :rtype: NoneType
        """
        self.pc_sel = sel

    def update_pc(self):
        """
        Update the program counter according to the current selection.

        :return: None
        :rtype: NoneType
        """
        if self.pc_sel:
            self.prog_counter.offset(self.get_alu_output())  # alu_out
        else:
            self.increment_pc()

    def get_alu_output(self):
        """
        Get the output of the ALU.

        :return: The output of the ALU
        :rtype: int
        """
        return self.alu.get_output()

    def get_immediate(self):
        """
        Get the current immediate value.

        :return: The current immediate value
        :rtype: int
        """
        return self.immediate_generator.get_immediate()

    def increment_pc(self):
        """
        Increment the program counter by 4 (1 instruction).

        :return: None
        :rtype: NoneType
        """
        self.prog_counter.increment()

    def split_instruction(self):
        """
        Split the current instruction into its components and pass them to the corresponding components.

        :return: The destination register address, source register 1 address, source register 2 address and immediate
        value
        :rtype: tuple
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
        :rtype: int
        """
        return self.reg_files.get_value_rs1()

    def get_value_rs2(self):
        """
        Get the value of source register 2.

        :return: The value of source register 2
        :rtype: int
        """
        return self.reg_files.get_value_rs2()

    def get_value_rd(self):
        """
        Get the value of destination register.

        :return: The value of destination register
        :rtype: int
        """
        return self.reg_files.get_value_rd()

    def set_reg_w_en(self, enable):
        """
        Sets the enable signal to write in register files.

        :param enable: enable signal to write in registers
        :type enable: bool
        :return: None
        :rtype: NoneType
        """
        self.reg_files.set_write_enable(enable)

    def compare(self, uns):
        """
        Performs the comparison between rs1 and rs2 values using the branch comparator.

        :param uns: tells the comparator if the comparison should be performed treating the numbers as unsigned.
        :type uns: bool
        :return: signals to control unit with the result of the comparison
        :rtype: tuple
        """
        data_rs1 = self.get_value_rs1()
        data_rs2 = self.get_value_rs2()
        self.branch_comparator.pass_inputs(data_rs1, data_rs2)
        if uns:
            self.branch_comparator.set_unsigned()
        self.branch_eq, self.branch_lt = self.branch_comparator.compare()
        return self.branch_eq, self.branch_lt

    def pass_alu_inputs(self, a_sel, b_sel):
        """
        Pass the appropriate inputs to the ALU depending on the current instruction.

        :param a_sel: selects the input of the ALU (0 - rs1, 1 - pc)
        :type a_sel: int
        :param b_sel: selects the second input of the ALU (0 - rs2, 1 - imm[31:0])
        :type b_sel: int
        :return: None
        :rtype: NoneType
        """
        a = self.get_pc() if a_sel else self.get_value_rs1()
        b = self.get_immediate() if b_sel else self.get_value_rs2()
        self.alu.pass_inputs(a, b)

    def set_alu_operation(self, operation):
        """
        Sets ALU operation based on current instruction.

        :param operation: operation to be performed by ALU
        :type operation: str
        :return: None
        :rtype: NoneType
        """
        self.alu.set_select(operation)

    def operate(self):
        """
        Performs operation in ALU.

        :return: output of the operation
        :rtype: int
        """
        return self.alu.operate()

    # mem_rw 0 read 1 write
    def set_mem_rw(self, mem_rw):
        """
        Sets the enable signal to write/read in data memory. (0 - read, 1 - write)

        :param mem_rw: enable signal to write/read in data memory.
        :type mem_rw: int
        :return: None
        :rtype: NoneType
        """
        self.data_mem.set_enable(write=mem_rw, read=not mem_rw)

    def set_imm_sel(self, imm_sel):
        """
        Sets immediate selection to change mode of operation of immediate generator. Depends on instruction.

        :param imm_sel: mode of operation of immediate generator.
        :type imm_sel: str
        :return: None
        :rtype: NoneType
        """
        self.immediate_generator.set_selection(imm_sel)

    def load_from_memory(self, size, uns):
        """
        Loads a value from the data memory into a register.

        :param size: size of load (1 - byte, 2 - halfword, 4 - word)
        :type size: int
        :param uns: flag to load number as unsigned
        :type uns: bool
        :return: value loaded from memory
        :rtype: int
        """
        address = self.operate()
        value = self.data_mem.load(address, size, uns)
        self.reg_files.write(value)
        return value

    def load_from_alu(self):
        """
        Loads the ALU output into a register.

        :return: None
        :rtype: NoneType
        """
        self.reg_files.write(self.operate())

    def load_from_pc(self):
        """
        Loads the value of PC + 4 into a register.

        :return: None
        :rtype: NoneType
        """
        self.reg_files.write(self.get_pc() + 4)

    def store_into_memory(self, size):
        """
        Stores a value from a register into a data memory address.

        :param size: size of value to store (1 - byte, 2 - halfword, 4 - word)
        :type size: int
        :return: value stored
        :rtype: int
        """
        address = self.operate()
        value = self.get_value_rs2()
        return self.data_mem.store(address, value, size)

    def set_wb_sel(self, value):
        """
        Sets the WBSel flag, a signal to decide what to write in the register files (0 - mem_out, 1 - alu_out,
        2 - pc + 4).

        :param value: enable signal
        :type value: int
        :return: None
        :rtype: NoneType
        """
        self.wb_sel = value

    def write_back(self, size, uns):
        """
        Write a value into a register based on instruction.

        :param size: size of value (1 - byte, 2 - halfword, 4 - word)
        :type size: int
        :param uns: flag to write the value as an unsigned number
        :type uns: bool
        :return: None
        :rtype: NoneType
        :raises: ValueError if the WBSel is invalid.
        """
        if self.wb_sel == 0:
            return self.load_from_memory(size, uns)
        elif self.wb_sel == 1:
            return self.load_from_alu()
        elif self.wb_sel == 2:
            return self.load_from_pc()
        else:
            raise ValueError("Invalid option for WBSel!")

    def load_instructions_from_file(self, file):
        """
        Load instructions from binary file into the instruction memory.
        :param file: binary file containing instructions
        :type file: file
        :return: list of instructions
        :rtype: list
        """
        return self.inst_mem.load_instructions_from_file(file)

    def load_instructions_from_asm_file(self, file):
        """
        Load instructions from RISC-V Assembly file into the instruction memory.
        :param file: asm file containing instructions
        :type file: file
        :return: list of instructions
        :rtype: list
        """
        return self.inst_mem.load_instructions_from_asm_file(file)

    def print_registers(self):
        """
        Prints the content of all registers.

        :return: None
        :rtype: NoneType
        """
        self.reg_files.print_all()

    def print_data_memory(self):
        """
        Prints the content of data memory.

        :return: None
        :rtype: NoneType
        """
        self.data_mem.print_data()

    def print_instructions(self):
        """
        Prints the content of instruction memory.

        :return: None
        :rtype: NoneType
        """
        self.inst_mem.print_instructions()

    def set_signals(
        self,
        a_sel,
        pc_sel,
        b_sel,
        wb_sel,
        mem_rw,
        alu_sel,
        imm_sel,
        branch_unsigned,
        reg_w_en,
        size,
        load_unsigned,
    ):
        """
        Sets all signals with the values from control unit.

        :param a_sel: selects the input of the ALU (0 - rs1, 1 - pc)
        :type a_sel: int
        :param pc_sel: selects the input of PC (0 - branch not taken or normal instruction - PC + 4, 1 - pc = alu_out)
        :type pc_sel: int
        :param b_sel: selects the second input of the ALU (0 - rs2, 1 - imm[31:0])
        :type b_sel: int
        :param wb_sel: enable signal to decide what to write in the register files
        (0 - mem_out, 1 - alu_out, 2 - pc + 4)
        :type wb_sel: int
        :param mem_rw: enable signal to write or read data into/of data memory (0 - read, 1 - write)
        :type mem_rw: int
        :param alu_sel: stores the operation to be performed in the ALU
        :type alu_sel: str
        :param imm_sel: stores the mode of operation for the immediate generator
        :type imm_sel: str
        :param branch_unsigned: signal to branch comparator if the comparison must be done between unsigned numbers
        :type branch_unsigned: bool
        :param reg_w_en: enable signal to allow writing in the register files
        :type reg_w_en: bool
        :param size: stores the size of a 'load' or 'store' instruction (1 - BYTE, 2 - HALFWORD, 4 - WORD)
        :type size: int
        :param load_unsigned: True if the load should be performed with unsigned number (sign extend to 0)
        :type load_unsigned: bool
        :return: None
        :rtype: NoneType
        """
        self.reg_w_en = reg_w_en
        self.mem_rw = mem_rw
        self.pc_sel = pc_sel
        self.wb_sel = wb_sel
        self.imm_sel = imm_sel.value
        self.branch_unsigned = branch_unsigned
        self.a_sel = a_sel
        self.b_sel = b_sel
        self.alu_sel = alu_sel
        self.store_size = size
        self.load_size = size
        self.load_unsigned = load_unsigned
