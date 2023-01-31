from utils.mask_bits import mask_bits
from utils.sign_extend import sign_extend

# TODO: tests
class DataMemory:
    """
    This class represents a data memory for a RISC-V single cycle processor model.
    """
    BYTE = 1
    HALF_WORD = 2
    WORD = 4

    def __init__(self, words=32):
        """
        Initialize the data memory with a given number of words

        :param words: The number of words the data memory has.
        """
        self.data = [0] * 4 * words
        self.data_in = None
        self.data_out = None
        self.write_enable = False
        self.read_enable = False
        self.words = words

    def get_value(self, address):
        """
        Get the value stored in a specific memory address.

        :param address: The memory address to retrieve the value from.
        :return: The value stored in the given memory address.
        """
        return self.data[address]

    def set_enable(self, write=True, read=True):
        """
        Set the write and read enable flags for the data memory.

        :param write: Boolean value indicating whether writing to the memory should be enabled.
        :param read: Boolean value indicating whether reading from the memory should be enabled.
        """
        self.write_enable = write
        self.read_enable = read

    def load(self, address, size, uns):
        """
        Loads a value from memory at a given address and size.

        :param uns: Zero-extends the output if set.
        :param address: The address of the memory location to be loaded.
        :type address: int
        :param size: The size of the value to be loaded. Must be one of
                     DataMemory.BYTE - 1, DataMemory.HALF_WORD - 2, or DataMemory.WORD - 4.
        :type size: int
        :return: The value stored at the given address and size, or a string
                 'Read Enable is unset!' if read enable is not set.
        :raises: ValueError if the size is not one of the specified constants.
                  IndexError if the address and size result in accessing memory
                  out of bounds.
        """
        if not self.read_enable:
            return 'Read Enable is unset!'
        elif size not in (DataMemory.BYTE, DataMemory.HALF_WORD, DataMemory.WORD):
            raise ValueError(f"Invalid size argument ({size}), must be DataMemory.BYTE, "
                             "DataMemory.HALF_WORD, or DataMemory.WORD!")
        elif address + size - 1 >= len(self.data):
            raise IndexError(f'Accessing out of bounds address ({address + size - 1}) in data memory!')
        elif address % 4 != 0:
            raise IndexError(f'Invalid address ({address}). Must be a multiple of 4!')
        else:
            self.data_out = 0
            for i in range(size):
                self.data_out |= self.data[address + i] << (8 * i)
            # return self.data_out if uns else sign_extend(self.data_out, size=size*8, sign=((self.data_out >> (size
            # * 8 - 1)) & 1))
            return self.data_out if uns else sign_extend(self.data_out, size=size * 8)

    def store(self, address, value, size):
        """
        Stores a value to the data memory at a specified address.

        :param address: The address in data memory to store the value.
        :type address: int
        :param value: The value to be stored in data memory.
        :type value: int
        :param size: The size of the value to be stored, must be DataMemory.BYTE,
                     DataMemory.HALF_WORD, or DataMemory.WORD.
        :type size: int
        :return: The value stored in data memory, or a string "Write Enable is unset!"
                 if the write enable is not set.
        :raises ValueError: If the size argument is invalid or the value is greater
                           than the maximum value for the specified size.
        :raises IndexError: If the address is out of bounds for the specified size.
        """
        if not self.write_enable:
            return 'Write Enable is unset!'
        elif size not in (DataMemory.BYTE, DataMemory.HALF_WORD, DataMemory.WORD):
            raise ValueError(f"Invalid size argument {(size)}, must be DataMemory.BYTE, "
                             "DataMemory.HALF_WORD, or DataMemory.WORD!")
        elif address % 4 != 0:
            raise IndexError(f'Invalid address ({address}). Must be a multiple of 4!')
        elif size == DataMemory.BYTE:
            #if value > 0xFF:
            #    raise ValueError(f'Value ({value}) is greater than 0xFF.')
            self.data_in = mask_bits(value, 0, 7)
            if address >= len(self.data):
                raise IndexError(f'Accessing out of bounds address ({address}) in data memory!')
            self.data[address] = self.data_in
            return self.data[address]
        elif size == DataMemory.HALF_WORD:
            #if value > 0xFFFF:
            #    raise ValueError(f'Value ({value}) is greater than 0xFFFF.')
            self.data_in = mask_bits(value, 0, 15)
            if address + 1 >= len(self.data):
                raise IndexError(f'Accessing out of bounds address ({address}) in data memory!')
            self.data[address] = mask_bits(self.data_in, 0, 7)
            self.data[address + 1] = mask_bits(self.data_in, 8, 15)
            return self.data[address] | (self.data[address + 1] << 8)
        elif size == DataMemory.WORD:
            if value > 0xFFFFFFFF:
                raise ValueError(f'Value ({value}) is greater than 0xFFFFFFFF.')
            self.data_in = value
            if address + 3 >= len(self.data):
                raise IndexError(f'Accessing out of bounds address ({address}) in data memory!')
            self.data[address] = mask_bits(self.data_in, 0, 7)
            self.data[address + 1] = mask_bits(self.data_in, 8, 15)
            self.data[address + 2] = mask_bits(self.data_in, 16, 23)
            self.data[address + 3] = mask_bits(self.data_in, 24, 31)
            return (self.data[address] | (self.data[address + 1] << 8) |
                    (self.data[address + 2] << 16) | (self.data[address + 3] << 24))

    def print_data(self):
        """
        Prints the contents of data memory, with each line showing the address in hexadecimal and its value.

        :return: None
        """
        for i in range(len(self.data)):
            print('Pos {:0X}: 0x{:04X}'.format(i, self.get_value(i)))

    def clear_memory(self):
        """
        Clears the contents of data memory by setting all memory locations to 0.

        :return: None
        """
        self.data = [0] * 4 * self.words
