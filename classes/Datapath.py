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
    def __init__(self, inst_mem: InstructionMemory = None,
                 prog_counter: ProgramCounter = None,
                 reg_files: RegisterFiles = None,
                 alu: ALU = None,
                 data_mem: DataMemory = None,
                 branch_comparator: BranchComparator = None,
                 immediate_generator: ImmediateGenerator = None):
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
        self.current_instruction = self.inst_mem.fetch_instruction(self.prog_counter.get_value())
        return self.current_instruction

    def get_pc(self):
        return self.prog_counter.get_value()

    def set_pc_sel(self, sel):
        self.pc_sel = sel

    def update_pc(self):
        if self.pc_sel:
            self.prog_counter.offset(self.get_alu_output())  # alu_out
        else:
            self.increment_pc()

    def get_alu_output(self):
        return self.alu.get_output()


    def get_immediate(self):
        return self.immediate_generator.get_immediate()

    def increment_pc(self):
        self.prog_counter.increment()

    def split_instruction(self):
        rs1 = mask_bits(self.current_instruction, 15, 19)
        rs2 = mask_bits(self.current_instruction, 20, 24)
        rd = mask_bits(self.current_instruction, 7, 11)
        self.reg_files.set_addresses(rd, rs1, rs2)
        imm = mask_bits(self.current_instruction, 7, 31)
        self.immediate_generator.pass_immediate(imm)
        return rd, rs1, rs2, imm

    def get_value_rs1(self):
        return self.reg_files.get_value_rs1()

    def get_value_rs2(self):
        return self.reg_files.get_value_rs2()

    def get_value_rd(self):
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






im = InstructionMemory(32)
im.fill_memory([3, 2, 1])
pc = ProgramCounter()
rf = RegisterFiles(32)
alu = ALU()
dm = DataMemory(32)
dp = Datapath(im, pc, rf, alu, dm)
x = dp.fetch_current_instruction()
print(x)
dp.increment_pc()
x = dp.fetch_current_instruction()
print(x)