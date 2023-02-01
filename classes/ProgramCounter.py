class ProgramCounter:
    """
    A class that represents a program counter for a RISC-V single cycle processor model.

    The program counter (PC) is a special register in a CPU that contains the address of the next instruction that
    will be executed.

    Attributes:
        value (int): The current value of the program counter.

    Methods:
        increment(): Increments the value of the program counter by 4.
        offset(offset: int): Offsets the value of the program counter by
                             the given offset if the offset is multiple of 2.
        set_value(value: int): Puts a given value in PC.
        get_value(): Returns the current value of the program counter.
    """

    def __init__(self, value=0):
        """
        Constructor method
        :param value: address of the first instruction to be executed (default : 0)
        :type value: int, optional
        """
        self.value = value

    def increment(self):
        """
        Increments the PC, setting its value to point to the next instruction (4 bytes away).

        :return: None
        :rtype: NoneType
        """
        self.value += 4

    def offset(self, offset):
        """
        Sets the value of PC to a given offset.

        :param offset: value of the offset
        :type offset: int
        :return: None
        :rtype: NoneType
        :raises: ValueError if new address is not a multiple of 4.
        """
        if offset % 4 == 0:
            self.value = offset
        else:
            raise ValueError("Offset must be multiple of 4!")

    def set_value(self, value):
        """
        Sets the value of PC.
        TODO: check if method is obsolete and duplicates offset().

        :param value: new value of PC
        :type value: int
        :return: None
        :rtype: NoneType
        """
        self.value = value

    def get_value(self):
        """
        Gets the current value of PC.

        :return: current value of PC
        :rtype: int
        """
        return self.value
