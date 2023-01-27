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
        self.write_enable = False
        self.out_1 = None
        self.out_2 = None
        self.addr_s1 = None
        self.addr_s2 = None
        self.addr_dest = None
        self.data_in = None

    def write(self, value):
        if not self.write_enable:
            return 'Write Enable is unset!'
        else:
            self.regs[self.addr_dest].write(value)

    # TODO: error handling
    def get_value_rs1(self):
        return self.regs[self.addr_s1].value

    def get_value_rs2(self):
        return self.regs[self.addr_s2].value

    def get_value_rd(self):
        return self.regs[self.addr_dest].value

    def get_value(self, key):
        return self.regs[key].get_value()

    def set_addresses(self, addr_dest, addr_s1, addr_s2):
        self.addr_dest = addr_dest
        self.addr_s1 = addr_s1
        self.addr_s2 = addr_s2
        return addr_dest, addr_s1, addr_s2

    def set_write_enable(self, en):
        self.write_enable = en

    def print_all(self):
        for i in range(self.size):
            print('Reg {}: {}'.format(i, self.get_value(i)))

