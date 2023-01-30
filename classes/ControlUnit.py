from classes.InstructionType import InstructionType
from utils.mask_bits import mask_bits


class ControlUnit:
    def __init__(self):
        self.operation = None
        self.alu_sel = None  # ALUSel (operation selection for ALU)
        self.imm_sel = None  # ImmSel (mode of operation for immediate generator)
        self.b_sel = None  # BSel (select in_2 of ALU (0 -> rs2, 1 -> imm[31:0]))
        self.mem_rw = None  # MemRW (Read or Write data of/in Data Memory, 0 -> read, 1 -> write)
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
        self.set_signals()

    def get_signals(self):
        return self.a_sel, self.pc_sel, self.b_sel, self.wb_sel, self.mem_rw, self.alu_sel, \
               self.imm_sel, self.branch_unsigned, self.reg_w_enable, self.size, self.load_unsigned

    def print_signals(self):
        print(f'PCSel: {self.pc_sel}')
        print(f'ImmSel: {self.imm_sel}')
        print(f'RegWEn: {self.reg_w_enable}')
        print(f'BrUn: {self.branch_unsigned}')
        print(f'BSel: {self.b_sel}')
        print(f'ASel: {self.a_sel}')
        print(f'ALUSel: {self.alu_sel}')
        print(f'MemRW: {self.mem_rw}')
        print(f'WBSel: {self.wb_sel}')
        print(f'Size: {self.size}')
        print(f'Unsigned load: {self.load_unsigned}')

    def set_signals(self):
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

    def set_a_sel(self):
        if self.inst_type in [InstructionType.UJ, InstructionType.SB]:
            self.a_sel = 1
        else:
            self.a_sel = 0

    def set_pc_sel(self):
        if self.branch_equal or self.branch_less_than:
            self.pc_sel = 1
        else:
            self.pc_sel = 0

    def set_branch_unsigned(self):
        if self.inst_type == InstructionType.R and self.funct3 in [0x6, 0x7]:
            self.branch_unsigned = True
        else:
            self.branch_unsigned = False

    def set_reg_w_enable(self):
        if self.inst_type in [InstructionType.S, InstructionType.SB, InstructionType.U]:
            self.reg_w_enable = False
        else:
            self.reg_w_enable = True

    def set_wb_sel(self):
        if self.inst_load:
            self.wb_sel = 0
        elif self.inst_jalr:
            self.wb_sel = 2
        else:
            self.wb_sel = 1

    def set_alu_sel(self):
        self.alu_sel = self.operation

    def set_imm_sel(self):
        self.imm_sel = self.inst_type

    def set_b_sel(self):
        if self.inst_type in [InstructionType.I, InstructionType.S, InstructionType.SB, InstructionType.U]:
            self.b_sel = 1
        else:
            self.b_sel = 0

    def set_mem_rw(self):
        if self.inst_type == InstructionType.S:
            self.mem_rw = 1
        else:
            self.mem_rw = 0

    def fetch_instruction(self, inst):
        self.instruction = inst
        return self.instruction

    def get_info_from_instruction(self):
        self.inst_opcode = mask_bits(self.instruction, 0, 6)
        self.funct3 = mask_bits(self.instruction, 12, 14)
        self.funct7 = mask_bits(self.instruction, 25, 31)
        return self.inst_opcode, self.funct3, self.funct7

    def get_type(self):
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
            raise ValueError(f'Invalid instruction! Opcode ({self.inst_opcode}) not supported!')

    def get_operation(self):
        if self.inst_type == InstructionType.R:
            if self.funct7 == 0x00:
                if self.funct3 == 0x0:
                    self.operation = 'add'
                elif self.funct3 == 0x4:
                    self.operation = 'xor'
                elif self.funct3 == 0x6:
                    self.operation = 'or'
                elif self.funct3 == 0x7:
                    self.operation = 'and'
                elif self.funct3 == 0x1:
                    self.operation = 'sll'
                elif self.funct3 == 0x5:
                    self.operation = 'srl'
                elif self.funct3 == 0x2:
                    self.operation = 'slt'
                elif self.funct3 == 0x3:
                    self.operation = 'sltu'
                else:
                    raise ValueError('Invalid funct3 {} for funct7 = 0x00'.format(self.funct3))
            elif self.funct7 == 0x20:
                if self.funct3 == 0x0:
                    self.operation = 'sub'
                elif self.funct3 == 0x5:
                    self.operation = 'sra'
                else:
                    raise ValueError('Invalid funct3 for funct7 = 0x20'.format(self.funct3))
            else:
                raise ValueError('Invalid funct7 {}!'.format(self.funct7))
        elif self.inst_type == InstructionType.I and not self.inst_load and not self.inst_jalr:
            if self.funct3 == 0x0:
                self.operation = 'add'
            elif self.funct3 == 0x4:
                self.operation = 'xor'
            elif self.funct3 == 0x6:
                self.operation = 'or'
            elif self.funct3 == 0x7:
                self.operation = 'and'
            elif self.funct3 == 0x1 and self.funct7 == 0x00:
                self.operation = 'sll'
            elif self.funct3 == 0x5 and self.funct7 == 0x00:
                self.operation = 'srl'
            elif self.funct3 == 0x5 and self.funct7 == 0x20:
                self.operation = 'sra'
            elif self.funct3 == 0x2:
                self.operation = 'slt'
            elif self.funct3 == 0x3:
                self.operation = 'sltu'
            else:
                raise ValueError('Invalid combination of funct3 ({}) and funct7 ({})'.format(self.funct3, self.funct7))
        elif self.inst_type in [InstructionType.UJ, InstructionType.U, InstructionType.S, InstructionType.SB] or \
                self.inst_load or self.inst_jalr:
            self.operation = 'add'
        else:
            raise ValueError('Invalid Instruction Type ({})!'.format(self.inst_type))

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
