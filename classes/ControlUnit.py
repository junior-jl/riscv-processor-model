from classes.InstructionType import InstructionType
from utils.mask_bits import mask_bits


class ControlUnit:
    """
    A ControlUnit class models the control unit of a RISC-V processor. It holds information about the control signals
    for various units in the processor, such as ALU operation, data memory operation, register file write enable, etc.

    Signals:
        - comparison_type - declares the type of branch instruction (equal, less than, greater or equal, not equal)
        - operation - stores the operation to be performed in the datapath ALU
        - alu_sel - stores the operation to be performed in the datapath ALU (TODO: update to avoid duplicate)
        - imm_sel - stores the mode of operation for the immediate generator
        - b_sel - selects the second input of the ALU (0 - rs2, 1 - imm[31:0])
        - mem_rw - enable signal to write or read data into/of data memory (0 - read, 1 - write)
        - wb_sel - enable signal to decide what to write in the register files (0 - mem_out, 1 - alu_out, 2 - pc + 4)
        - reg_w_enable - enable signal to allow writing in the register files
        - branch_unsigned - signal to branch comparator if the comparison must be done between unsigned numbers
        - branch_equal - input (True if rs1 == rs2)
        - branch_less_than - input (True if rs1 < rs2)
        - a_sel - selects the input of the ALU (0 - rs1, 1 - pc)
        - pc_sel - selects the input of PC (0 - branch not taken or normal instruction - PC + 4, 1 - pc = alu_out)
        - instruction - current instruction
        - inst_opcode - current instruction opcode
        - funct3 - current instruction funct3 field
        - funct7 - current instruction funct7 field
        - inst_type - current instruction type
        - inst_load - True if current instruction is a load
        - inst_jalr - True if current instruction is 'jalr'
        - size - stores the size of a 'load' or 'store' instruction (1 - BYTE, 2 - HALFWORD, 4 - WORD)
        - load_unsigned - True if the load should be performed with unsigned number (sign extend to 0)
    """

    def __init__(self):
        """
        Constructor method
        """
        self.comparison_type = None
        self.operation = None
        self.alu_sel = None  # ALUSel (operation selection for ALU)
        self.imm_sel = None  # ImmSel (mode of operation for immediate generator)
        self.b_sel = None  # BSel (select in_2 of ALU (0 -> rs2, 1 -> imm[31:0]))
        self.mem_rw = (
            None  # MemRW (Read or Write data of/in Data Memory, 0 -> read, 1 -> write)
        )
        self.wb_sel = None  # WBSel (Write-back select | What is written to a register (0 -> mem_out, 1 -> alu_out,
        # 2 -> pc + 4))
        self.reg_w_enable = None  # RegWEn (Enable writing in the register files)
        self.branch_unsigned = None  # BrUn (True if comparison is done between unsigned ints, False otherwise)
        self.branch_equal = None  # BrEq (input -> True if rs1 == rs2)
        self.branch_less_than = None  # BrLT (input -> True if rs1 < rs2)
        self.a_sel = None  # ASel (select in_1 of ALU (0 -> rs1, 1 -> pc))
        self.pc_sel = None  # PCSel (Depends on branch (0 -> branch not taken pc += 4, 1 -> branch taken pc = alu_out))
        self.instruction = 0
        self.inst_opcode = 0
        self.funct3 = 0
        self.funct7 = 0
        self.inst_type = None
        self.inst_load = False
        self.inst_jalr = False
        self.size = 0
        self.load_unsigned = 0

    def reset(self):
        """
        Resets the control signals.
        TODO: update constructor method to use this method instead of repetition.

        :return: None
        :rtype: NoneType
        """
        self.comparison_type = None
        self.operation = None
        self.alu_sel = None  # ALUSel (operation selection for ALU)
        self.imm_sel = None  # ImmSel (mode of operation for immediate generator)
        self.b_sel = None  # BSel (select in_2 of ALU (0 -> rs2, 1 -> imm[31:0]))
        self.mem_rw = (
            None  # MemRW (Read or Write data of/in Data Memory, 0 -> read, 1 -> write)
        )
        self.wb_sel = None  # WBSel (Write-back select | What is written to a register (0 -> mem_out, 1 -> alu_out,
        # 2 -> pc + 4))
        self.reg_w_enable = None  # RegWEn (Enable writing in the register files)
        self.branch_unsigned = None  # BrUn (True if comparison is done between unsigned ints, False otherwise)
        self.branch_equal = None  # BrEq (input -> True if rs1 == rs2)
        self.branch_less_than = None  # BrLT (input -> True if rs1 < rs2)
        self.a_sel = None  # ASel (select in_1 of ALU (0 -> rs1, 1 -> pc))
        self.pc_sel = None  # PCSel (Depends on branch (0 -> branch not taken pc += 4, 1 -> branch taken pc = alu_out))
        self.instruction = 0
        self.inst_opcode = 0
        self.funct3 = 0
        self.funct7 = 0
        self.inst_type = None
        self.inst_load = False
        self.inst_jalr = False
        self.size = 0
        self.load_unsigned = 0

    def run(self):
        """
        Does the control unit operation, setting the control signals.

        :return: None
        :rtype: NoneType
        """
        self.set_signals()

    def get_signals(self):
        """
        Returns the control signals of the control unit.

        :return: a tuple with the control signals
        :rtype: tuple
        """
        return (
            self.a_sel,
            self.pc_sel,
            self.b_sel,
            self.wb_sel,
            self.mem_rw,
            self.alu_sel,
            self.imm_sel,
            self.branch_unsigned,
            self.reg_w_enable,
            self.size,
            self.load_unsigned,
        )

    def print_signals(self):
        """
        Prints all the control signals.

        :return: None
        :rtype: NoneType
        """
        print(f"PCSel: {self.pc_sel}")
        print(f"ImmSel: {self.imm_sel}")
        print(f"RegWEn: {self.reg_w_enable}")
        print(f"BrUn: {self.branch_unsigned}")
        print(f"BSel: {self.b_sel}")
        print(f"ASel: {self.a_sel}")
        print(f"ALUSel: {self.alu_sel}")
        print(f"MemRW: {self.mem_rw}")
        print(f"WBSel: {self.wb_sel}")
        print(f"Size: {self.size}")
        print(f"Unsigned load: {self.load_unsigned}")

    def set_signals(self):
        """
        Set the control signals based on the current instruction.

        :return: None
        :rtype: NoneType
        """
        self.get_info_from_instruction()
        self.get_type()
        self.get_operation()
        self.set_a_sel()
        self.set_pc_sel()
        self.set_b_sel()
        self.set_wb_sel()
        self.set_mem_rw()
        self.set_alu_sel()
        self.set_imm_sel()
        self.set_branch_unsigned()
        self.set_reg_w_enable()
        self.set_size()

    def set_size(self):
        """
        Sets the size of load/store based on the instruction. (1 - BYTE, 2 - HALFWORD, 4 - WORD)

        :return: None
        :rtype: NoneType
        """
        if self.funct3 == 0x0:
            self.size = 1
            self.load_unsigned = False
        elif self.funct3 == 0x1:
            self.size = 2
            self.load_unsigned = False
        elif self.funct3 == 0x2:
            self.size = 4
            self.load_unsigned = False
        elif self.funct3 == 0x4:
            self.size = 1
            self.load_unsigned = True
        elif self.funct3 == 0x5:
            self.size = 2
            self.load_unsigned = True

    def set_comparison_type(self):
        """
        Sets and returns the comparison type based on current instruction (beq, bne, blt, bge).

        :return: the comparison type of the instruction
        :rtype: str
        """
        if self.inst_opcode == 0x63:
            if self.funct3 == 0x0:
                self.comparison_type = "beq"
            elif self.funct3 == 0x1:
                self.comparison_type = "bne"
            elif self.funct3 in [0x4, 0x6]:
                self.comparison_type = "blt"
            elif self.funct3 in [0x5, 0x7]:
                self.comparison_type = "bge"
            else:
                self.comparison_type = None
        else:
            self.comparison_type = None
        return self.comparison_type

    def set_a_sel(self):
        """
        Sets ASel based on instruction. (0 - rs1, 1 - pc)

        :return: None
        :rtype: NoneType
        """
        if (
            self.inst_type in [InstructionType.UJ, InstructionType.SB]
            or self.inst_opcode == 0x17
        ):
            self.a_sel = 1
        else:
            self.a_sel = 0

    def branch(self, eq, lt):
        """
        Sets and returns branch signals based on input from datapath.
        :param eq: result of comparison for equality
        :type eq: bool
        :param lt: result of comparison for less than
        :type lt: bool
        :return: signals for comparison flags
        :rtype: tuple
        """
        self.branch_equal = eq
        self.branch_less_than = lt
        return self.branch_equal, self.branch_less_than

    def branch_taken(self):
        """
        Returns True if branch was taken (i.e. if the comparison flag is true or false and matches the current
        comparison type).
        :return: result of boolean expression to check if branch should be taken
        :rtype: bool
        """
        return (
            (self.branch_equal and (self.set_comparison_type() == "beq"))
            or (self.branch_less_than and (self.set_comparison_type() == "blt"))
            or (not self.branch_equal and (self.set_comparison_type() == "bne"))
            or (not self.branch_less_than and (self.set_comparison_type() == "bge"))
        )

    def set_pc_sel(self):
        """
        Sets PCSel (0 - branch not taken or normal instruction -> PC + 4, 1 - branch taken or jump -> alu_out)

        :return: None
        :rtype: NoneType
        """
        if (
            self.inst_jalr
            or self.inst_type == InstructionType.UJ
            or self.branch_taken()
        ):
            # if self.branch_equal or self.branch_less_than or self.inst_jalr or self.inst_type == InstructionType.UJ:
            self.pc_sel = 1
        else:
            self.pc_sel = 0

    def set_branch_unsigned(self):
        """
        Sets BrUn (True if comparison must be done between unsigned numbers)

        :return: None
        :rtype: NoneType
        """
        if self.inst_type == InstructionType.R and self.funct3 in [0x6, 0x7]:
            self.branch_unsigned = True
        else:
            self.branch_unsigned = False

    def set_reg_w_enable(self):
        """
        Sets RegWEn (enable signal to write on register files)

        :return: None
        :rtype: NoneType
        """
        if self.inst_type in [InstructionType.S, InstructionType.SB]:
            self.reg_w_enable = False
        else:
            self.reg_w_enable = True

    def set_wb_sel(self):
        """
        Sets WBSel (enable signal to decide what to write in the register files (0 - mem_out, 1 - alu_out, 2 - pc + 4))

        :return: None
        :rtype: NoneType
        """
        if self.inst_load:
            self.wb_sel = 0
        elif self.inst_jalr or self.inst_type == InstructionType.UJ:
            self.wb_sel = 2
        else:
            self.wb_sel = 1

    def set_alu_sel(self):
        """
        Sets ALUSel (operation to be performed by the datapath ALU)

        :return: None
        :rtype: NoneType
        """
        self.alu_sel = self.operation

    def set_imm_sel(self):
        """
        Sets ImmSel (mode of operation for the immediate generator of the datapath)

        :return: None
        :rtype: NoneType
        """
        self.imm_sel = self.inst_type

    def set_b_sel(self):
        """
        Sets BSel (selects the second input of the ALU, 0 -> rs2, 1 -> imm[31:0])

        :return: None
        :rtype: NoneType
        """
        if self.inst_type is not InstructionType.R:
            self.b_sel = 1
        else:
            self.b_sel = 0

    def set_mem_rw(self):
        """
        Sets MemRW (enable signal to write or read data into/of data memory (0 - read, 1 - write))

        :return: None
        :rtype: NoneType
        """
        if self.inst_type == InstructionType.S:
            self.mem_rw = 1
        else:
            self.mem_rw = 0

    def fetch_instruction(self, inst):
        """
        Gets the current instruction.

        :param inst: current instruction on instruction memory
        :type inst: int
        :return: current instruction
        :rtype: int
        """
        self.instruction = inst
        return self.instruction

    def get_info_from_instruction(self):
        """
        Gets information from current instruction (opcode, funct3, funct7), used to decode it.
        :return: opcode, funct3 and funct7 of the instruction
        :rtype: tuple
        """
        self.inst_opcode = mask_bits(self.instruction, 0, 6)
        self.funct3 = mask_bits(self.instruction, 12, 14)
        self.funct7 = mask_bits(self.instruction, 25, 31)
        return self.inst_opcode, self.funct3, self.funct7

    def get_type(self):
        """
        Gets the type of currrent instruction (R, I, S, SB, UJ, U).

        :return: None
        :rtype: NoneType
        """
        if self.inst_opcode == 0x33:
            self.inst_type = InstructionType.R
        elif self.inst_opcode in [0x13, 0x03, 0x67]:
            self.inst_type = InstructionType.I
            if self.inst_opcode == 0x03:
                self.inst_load = True
                self.set_size()
            else:
                self.inst_load = False
            if self.inst_opcode == 0x67:
                self.inst_jalr = True
            else:
                self.inst_jalr = False
        elif self.inst_opcode == 0x23:
            self.inst_type = InstructionType.S
            self.set_size()
        elif self.inst_opcode == 0x63:
            self.inst_type = InstructionType.SB
        elif self.inst_opcode == 0x6F:
            self.inst_type = InstructionType.UJ
        elif self.inst_opcode in [0x37, 0x17]:
            self.inst_type = InstructionType.U
        else:
            raise ValueError(
                f"Invalid instruction! Opcode ({self.inst_opcode}) not supported!"
            )

    def get_operation(self):
        """
        Gets the operation to be performed by the ALU based on the current instruction type.

        :return: None
        :rtype: NoneType
        """
        if self.inst_type == InstructionType.R:
            if self.funct7 == 0x00:
                if self.funct3 == 0x0:
                    self.operation = "add"
                elif self.funct3 == 0x4:
                    self.operation = "xor"
                elif self.funct3 == 0x6:
                    self.operation = "or"
                elif self.funct3 == 0x7:
                    self.operation = "and"
                elif self.funct3 == 0x1:
                    self.operation = "sll"
                elif self.funct3 == 0x5:
                    self.operation = "srl"
                elif self.funct3 == 0x2:
                    self.operation = "slt"
                elif self.funct3 == 0x3:
                    self.operation = "sltu"
                else:
                    raise ValueError(
                        "Invalid funct3 {} for funct7 = 0x00".format(self.funct3)
                    )
            elif self.funct7 == 0x20:
                if self.funct3 == 0x0:
                    self.operation = "sub"
                elif self.funct3 == 0x5:
                    self.operation = "sra"
                else:
                    raise ValueError(
                        "Invalid funct3 for funct7 = 0x20".format(self.funct3)
                    )
            else:
                raise ValueError("Invalid funct7 {}!".format(self.funct7))
        elif (
            self.inst_type == InstructionType.I
            and not self.inst_load
            and not self.inst_jalr
        ):
            if self.funct3 == 0x0:
                self.operation = "add"
            elif self.funct3 == 0x4:
                self.operation = "xor"
            elif self.funct3 == 0x6:
                self.operation = "or"
            elif self.funct3 == 0x7:
                self.operation = "and"
            elif self.funct3 == 0x1 and self.funct7 == 0x00:
                self.operation = "sll"
            elif self.funct3 == 0x5 and self.funct7 == 0x00:
                self.operation = "srl"
            elif self.funct3 == 0x5 and self.funct7 == 0x20:
                self.operation = "sra"
            elif self.funct3 == 0x2:
                self.operation = "slt"
            elif self.funct3 == 0x3:
                self.operation = "sltu"
            else:
                raise ValueError(
                    "Invalid combination of funct3 ({}) and funct7 ({})".format(
                        self.funct3, self.funct7
                    )
                )
        elif (
            self.inst_type
            in [
                InstructionType.UJ,
                InstructionType.U,
                InstructionType.S,
                InstructionType.SB,
            ]
            or self.inst_load
            or self.inst_jalr
        ):
            self.operation = "add"
        else:
            raise ValueError("Invalid Instruction Type ({})!".format(self.inst_type))

    # R-Type
    #   ALUSel
    #   Write Enable

    # Arithmetic I-Type
    #   ALUSel
    #   Write Enable
    #   BSel (1)
    #   ImmSel
    #   Write Enable

    # Load I-Type
    #   MemRW
    #   WBSel
    #   ALUSel
    #   Write Enable

    # S-Type
    #   Write Enable (0)
    #   MemRW
    #   ALUSel (add)

    # SB-Type
    #   BrUn
    #   BrEq
    #   BrLT
    #   PCSel
    #   ASel

    # Jump I-Type (JALR)
    #   WBSel

    # J-Type
