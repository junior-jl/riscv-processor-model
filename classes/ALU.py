from utils.mask_bits import mask_bits
from utils.sign_extend import sign_extend, get_bit_size
from utils.unsigned import unsigned


class ALU:
    def __init__(self):
        self.in_1 = None
        self.in_2 = None
        self.select = None
        self.output = None

    def pass_inputs(self, a, b):
        self.in_1 = a
        self.in_2 = b

    def set_select(self, select_value):
        self.select = select_value

    def get_output(self):
        return self.output

    def operate(self):
        if self.select == 'add':
            self.output = self.in_1 + self.in_2
        elif self.select == 'sub':
            self.output = self.in_1 - self.in_2
        elif self.select == 'mul':
            self.output = self.in_1 * self.in_2
        elif self.select == 'div':
            self.output = self.in_1 / self.in_2
        elif self.select == 'and':
            self.output = self.in_1 & self.in_2
        elif self.select == 'or':
            self.output = self.in_1 | self.in_2
        elif self.select == 'xor':
            self.output = self.in_1 ^ self.in_2
        elif self.select == 'not':
            self.output = ~self.in_1
        elif self.select == 'sll':
            self.output = self.in_1 << self.in_2
        elif self.select == 'srl':
            self.output = self.in_1 >> self.in_2
        elif self.select == 'slt':
            self.output = int(self.in_1 < self.in_2)
        elif self.select == 'sltu':
            self.output = int(unsigned(self.in_1) < unsigned(self.in_2))
        elif self.select == 'sra':
            # TODO: Make it better
            # imm[0:4] is the shift value
            # imm[5:11] is 0x20 and makes the value wrong
            self.in_2 = mask_bits(self.in_2, 0, 4)
            output = self.in_1 >> self.in_2
            size = get_bit_size(output)
            self.output = sign_extend(output, sign=mask_bits(output, size-self.in_2, size-self.in_2), size=size)
        else:
            self.output = None
        self.output = mask_bits(self.output, 0, 31)
        return self.output
