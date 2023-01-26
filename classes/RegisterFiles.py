class Register:
    """
    A class that represents a single register in a register file.
    """

    def __init__(self, key, value=0):
        """
        Initializes a new instance of the Register class.

        :param key: The key/index of the register
        :param value: The initial value of the register (default: 0)
        """
        self.key = key
        self.value = value

    def write(self, value):
        """
        Writes a value to the register.

        :param value: The value to be written to the register
        """
        self.value = value if self.key else 0

    def get_value(self):
        """
        Gets the current value of the register.

        :return: The current value of the register
        """
        return self.value


class RegisterFiles:
    """
    A class that represents a collection of registers in a register file.
    """

    def __init__(self, num_of_reg):
        """
        Initializes a new instance of the RegisterFiles class.

        :param num_of_reg: The number of registers in the register file
        """
        self.regs = []
        self.size = num_of_reg
        for i in range(num_of_reg):
            self.regs.append(Register(i))

    def write(self, key, value):
        """
        Writes a value to a register in the register file.

        :param key: The key/index of the register to write to
        :param value: The value to be written to the register
        """
        self.regs[key].write(value)

    def get_value(self, key):
        """
        Gets the current value of a register in the register file.

        :param key: The key/index of the register
        :return: The current value of the register
        """
        return self.regs[key].get_value()

    def print_all(self):
        for i in range(self.size):
            print('Reg {}: {}'.format(i, self.get_value(i)))
