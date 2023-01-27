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
        elif self.select == 'subtract':
            self.output = self.in_1 - self.in_2
        elif self.select == 'multiply':
            self.output = self.in_1 * self.in_2
        elif self.select == 'divide':
            self.output = self.in_1 / self.in_2
        elif self.select == 'and':
            self.output = self.in_1 & self.in_2
        elif self.select == 'or':
            self.output = self.in_1 | self.in_2
        elif self.select == 'xor':
            self.output = self.in_1 ^ self.in_2
        elif self.select == 'not':
            self.output = ~self.in_1
        elif self.select == 'left_shift':
            self.output = self.in_1 << self.in_2
        elif self.select == 'right_shift':
            self.output = self.in_1 >> self.in_2
        else:
            self.output = None
        return self.output
