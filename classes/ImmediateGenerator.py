from utils.sign_extend import sign_extend


class ImmediateGenerator:
    def __init__(self):
        self.imm_sel = None
        self.imm_in = None
        self.imm_out = None

    def set_selection(self, select_value):
        self.imm_sel = select_value

    def pass_immediate(self, num):
        self.imm_in = num

    def get_immediate(self):
        return self.imm_out

    def generate(self):
        if self.imm_sel == 'I':
            self.imm_out = sign_extend(self.imm_in, 32)
        else:
            raise ValueError('Not a valid value for ImmSel!')

