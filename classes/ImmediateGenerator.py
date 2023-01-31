from utils.mask_bits import mask_bits
from utils.sign_extend import sign_extend


class ImmediateGenerator:
    def __init__(self):
        self.imm_sel = None
        self.imm_in = None
        self.imm_out = None
        self.sign = None

    def set_selection(self, select_value):
        self.imm_sel = select_value

    def pass_immediate(self, inst_imm):
        self.sign = mask_bits(inst_imm, 24, 24)
        self.imm_in = inst_imm

    def get_immediate(self):
        self.generate()
        return self.imm_out

    # inst_imm = inst[7:31]
    # inst_imm has 25 bits (0 - 24) = (7 - 31)
    # I -> imm[0:11] = inst[20:31] = inst_imm[13:24]
    # S -> imm[5:11] = inst[25:31] = inst_imm[18:24]
    #      imm[0:4] = inst[7:11] = inst_imm[0:4]
    # SB -> imm[12] = inst[31] = inst_imm[24]
    #       imm[5:10] = inst[25:30] = inst_imm[18:23]
    #       imm[1:4] = inst[8:11] = inst_imm[1:4]
    #       imm[11] = inst[7] = inst_imm[0]
    # U -> imm[12:31] = inst[12:31] = inst_imm[5:24] (imm[0:11] = 0)
    # UJ -> imm[20] = inst[31] = inst_imm[24]
    #       imm[1:10] = inst[21:30] = inst_imm[14:23]
    #       imm[11] = inst[20] = inst_imm[13]
    #       imm[12:19] = inst[12:19] = inst_imm[5:12]
    def generate(self):
        num = 0
        if self.imm_sel == 'I':
            num |= mask_bits(self.imm_in, 13, 24)
            self.imm_out = sign_extend(num, sign=self.sign)
        elif self.imm_sel == 'S':
            num |= mask_bits(self.imm_in, 0, 4)
            num |= (mask_bits(self.imm_in, 18, 24) << 5)
            self.imm_out = sign_extend(num, sign=self.sign)
        elif self.imm_sel == 'SB':
            num |= (mask_bits(self.imm_in, 1, 4) << 1)
            num |= (mask_bits(self.imm_in, 18, 23) << 5)
            num |= (mask_bits(self.imm_in, 0, 0) << 11)
            num |= (mask_bits(self.imm_in, 24, 24) << 12)
            self.imm_out = sign_extend(num, sign=self.sign)
        elif self.imm_sel == 'U':
            num |= (mask_bits(self.imm_in, 5, 24) << 12)
            self.imm_out = num
        elif self.imm_sel == 'UJ':
            num |= (mask_bits(self.imm_in, 14, 23) << 1)
            num |= (mask_bits(self.imm_in, 13, 13) << 11)
            num |= (mask_bits(self.imm_in, 5, 12) << 12)
            num |= (mask_bits(self.imm_in, 24, 24) << 20)
            self.imm_out = sign_extend(num)
        else:
            self.imm_out = sign_extend(num, sign=self.sign)

        # else:
        #    raise ValueError('Not a valid value for ImmSel!')
