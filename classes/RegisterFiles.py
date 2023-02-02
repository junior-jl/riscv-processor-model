class Register:
    """
    A class that represents a single register in a register file on a RISC-V Processor.
    """

    def __init__(self, key=0, value=0):
        """
        Constructor method

        :param key: The key/index of the register
        :param value: The initial value of the register (default: 0)
        """
        self.key = key
        self.value = value

    def write(self, value):
        """
        Writes a value to the register.

        :param value: The value to be written to the register
        :type value: int
        :return: None
        :rtype: NoneType
        """
        self.value = value if self.key else 0

    def get_value(self):
        """
        Gets the current value of the register.

        :return: The current value of the register
        :rtype: int
        """
        return self.value


class RegisterFiles:
    """
    A class that represents a collection of registers in a RISC-V processor's register files.
    """

    def __init__(self, num_of_reg=32):
        """
        Constructor method

        :param num_of_reg: The number of registers in the register file (default: 32)
        :type num_of_reg: int
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
        """
        Writes the specified value to the register specified by `addr_dest` if `write_enable` is set.

        :param value: The value to be written to the register
        :type value: int
        :return: A string indicating that the write is not allowed if `write_enable` is not set
        :rtype: str
        """
        if not self.write_enable:
            return "Write Enable is unset!"
        else:
            self.regs[self.addr_dest].write(value)

    # TODO: error handling
    def get_value_rs1(self):
        """
        Gets the value stored in the register specified by the `addr_s1` address.

        :return: the value in rs1
        :rtype: int
        """
        return self.regs[self.addr_s1].value

    def get_value_rs2(self):
        """
        Gets the value stored in the register specified by the `addr_s2` address.

        :return: the value in rs2
        :rtype: int
        """
        return self.regs[self.addr_s2].value

    def get_value_rd(self):
        """
        Gets the value stored in the register specified by the `addr_dest` address.

        :return: the value in rd
        :rtype: int
        """
        return self.regs[self.addr_dest].value

    def get_value(self, key):
        """
        Returns the value of a register given its key.

        :param key: identification key for the register
        :type key: int
        :return: the value in the register
        :rtype: int
        """
        return self.regs[key].get_value()

    def set_addresses(self, addr_dest, addr_s1, addr_s2):
        """
        Sets the addresses of source and destination registers based on the current instruction.

        :param addr_dest: address of the destination register
        :type addr_dest: int
        :param addr_s1: address of the source register 1
        :type addr_s1: int
        :param addr_s2: address of the source register 2
        :type addr_s2: int
        :return: addresses of the given registers
        :rtype: tuple
        """
        self.addr_dest = addr_dest
        self.addr_s1 = addr_s1
        self.addr_s2 = addr_s2
        return addr_dest, addr_s1, addr_s2

    def set_write_enable(self, en):
        """
        Sets the enable flag to write in the register files.

        :param en: enable flag to write in register files
        :type en: bool
        :return: None
        :rtype: NoneType
        """
        self.write_enable = en

    def print_all(self):
        """
        Prints the contents of all the registers.

        :return: None
        :rtype: NoneType
        """
        for i in range(self.size):
            print("Reg {}: 0x{:08X}".format(i, self.get_value(i)))
