class ProgramCounter:
    """
    A class that represents a program counter.

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
        self.value = value

    def increment(self):
        self.value += 4

    def offset(self, offset):
        if offset % 2 == 0:
            self.value += offset
        else:
            raise ValueError("Offset must be multiple of 2!")

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value



