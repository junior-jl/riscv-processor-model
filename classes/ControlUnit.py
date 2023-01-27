class ControlUnit:
    def __init__(self):
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
