from utils.mask_bits import mask_bits
from utils.sign_extend import sign_extend, get_bit_size
from utils.unsigned import unsigned


class ALU:
    """
    The ALU class represents the arithmetic logic unit (ALU) of a RISC-V processor model. It gets two inputs,
    a selection value, perform an operation an returns an output.
    """

    def __init__(self):
        """
        Initialize the ALU inputs and output value.
        """
        self.in_1 = None
        self.in_2 = None
        self.select = None
        self.output = None

    def pass_inputs(self, a, b):
        """
        Pass the values of parameters a and b to the inputs of the ALU.

        :param a: first input for the ALU
        :type a: int
        :param b: second input for the ALU
        :type b: int
        :return: None
        :rtype: NoneType
        """
        self.in_1 = a
        self.in_2 = b

    def set_select(self, select_value):
        """
        Sets the selection input for the ALU, choosing the operation.

        :param select_value: the operation to be performed by the ALU
        :type select_value: str
        """
        self.select = select_value

    def get_output(self):
        """
        Returns the output value of the ALU.

        :return: the output value of the ALU
        :rtype: int
        """
        return self.output

    def operate(self):
        """
        Performs an operation with in_1 and in_2 based on the selection value.

        :return: the result of the operation as a 32-bit number
        :rtype: int
        """
        if self.select == "add":
            self.output = self.in_1 + self.in_2
        elif self.select == "sub":
            self.output = self.in_1 - self.in_2
        elif self.select == "mul":
            self.output = self.in_1 * self.in_2
        elif self.select == "div":
            self.output = self.in_1 / self.in_2
        elif self.select == "and":
            self.output = self.in_1 & self.in_2
        elif self.select == "or":
            self.output = self.in_1 | self.in_2
        elif self.select == "xor":
            self.output = self.in_1 ^ self.in_2
        elif self.select == "not":
            self.output = ~self.in_1
        elif self.select == "sll":
            self.output = self.in_1 << self.in_2
        elif self.select == "srl":
            self.output = self.in_1 >> self.in_2
        elif self.select == "slt":
            self.output = int(self.in_1 < self.in_2)
        elif self.select == "sltu":
            self.output = int(unsigned(self.in_1) < unsigned(self.in_2))
        elif self.select == "sra":
            # TODO: Make it better
            # imm[0:4] is the shift value
            # imm[5:11] is 0x20 and makes the value wrong
            self.in_2 = mask_bits(self.in_2, 0, 4)
            output = self.in_1 >> self.in_2
            size = get_bit_size(output)
            self.output = sign_extend(
                output,
                sign=mask_bits(output, size - self.in_2, size - self.in_2),
                size=size,
            )
        else:
            self.output = None
        self.output = mask_bits(self.output, 0, 31)
        return self.output
