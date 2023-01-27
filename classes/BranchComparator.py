from utils.unsigned import unsigned

class BranchComparator:
    def __init__(self):
        self.in_1 = None
        self.in_2 = None
        self.branch_unsigned = None
        self.branch_equal = None
        self.branch_less_than = None

    def pass_inputs(self, a, b):
        self.in_1 = a
        self.in_2 = b

    def compare(self):
        if self.branch_unsigned:
            self.branch_equal = (unsigned(self.in_1) == unsigned(self.in_2))
            self.branch_less_than = (unsigned(self.in_1) < unsigned(self.in_2))
        else:
            self.branch_equal = (self.in_1 == self.in_2)
            self.branch_less_than = (self.in_1 < self.in_2)
        return self.branch_equal, self.branch_less_than

    def set_unsigned(self):
        self.branch_unsigned = True


