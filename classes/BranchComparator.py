from utils.unsigned import unsigned


class BranchComparator:
    """
    This class represents a branch comparator for a RISC-V single cycle processor model. It compares two inputs and
    returns flags for the results.
    """

    def __init__(self):
        """
        Constructor method
        """
        self.in_1 = None
        self.in_2 = None
        self.branch_unsigned = None
        self.branch_equal = None
        self.branch_less_than = None

    def pass_inputs(self, a, b):
        """
        Pass the value of parameters a and b to the inputs of the comparator.

        :param a: first input for the comparator
        :type a: int
        :param b: second input for the comparator
        :type b: int
        :return: None
        :rtype: NoneType
        """
        self.in_1 = a
        self.in_2 = b

    def compare(self):
        """
        Do the comparison between the two inputs and returns flags based on result.

        :return: Result of 'equal' comparison, result of 'less than' comparison
        :rtype: tuple
        """
        if self.branch_unsigned:
            self.branch_equal = unsigned(self.in_1) == unsigned(self.in_2)
            self.branch_less_than = unsigned(self.in_1) < unsigned(self.in_2)
        else:
            self.branch_equal = self.in_1 == self.in_2
            self.branch_less_than = self.in_1 < self.in_2
        return self.branch_equal, self.branch_less_than

    def set_unsigned(self):
        """
        Sets the unsigned flag for the comparator. The flag tells the comparator should treat the inputs as unsigned
        integers.

        :return: None
        :rtype: NoneType
        """
        self.branch_unsigned = True
