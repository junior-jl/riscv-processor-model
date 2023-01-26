class Control:
    def __init__(self):
        self.alu_sel = None  # ALUSel (operation selection for ALU)
        self.imm_sel = None  # ImmSel (mode of operation for immediate generator)
        self.b_sel = None  # BSel (select in_2 of ALU (0 -> rs2, 1 -> imm[31:0]))
        self.mem_rw = None  # MemRW (Read or Write data of/in Data Memory)
        self.wb_sel = None  # WBSel (Write-back select | What is written to a register (0 -> mem_out, 1 -> alu_out))
