from utils.encode_instructions import encode_instructions
from utils.get_instructions_asm_file import get_instructions_asm_file
from utils.mask_bits import mask_bits
from utils.write_file_encoded_instructions import write_file_encoded_instructions


class InstructionMemory:
    """
    The InstructionMemory class models the instruction memory from a RISC-V Single Cycle Processor.

        instructions (list) - list of instructions encoded (32 bits)
        instructions_bytes (list) - list of instructions encoded (8 bits)
    """

    def __init__(self, words=32, encoded_instructions=None):
        """
        Constructor method

        :param words: number of words in the memory (instructions supported)
        :type words: int, optional
        :param encoded_instructions: list of binary encoded instructions
        :type encoded_instructions: list, optional
        """
        self.inst_out = None
        if not encoded_instructions:
            self.instructions = [0] * words
            self.instructions_bytes = [0] * words * 4
        else:
            self.instructions = [0] * len(encoded_instructions)
            self.instructions_bytes = [0] * 4 * len(encoded_instructions)
            self.fill_memory(encoded_instructions)

    def fetch_instruction(self, address):
        """
        Fetch instruction on given address.

        :param address: address of memory containing the instruction required
        :type address: int
        :return: instruction on the address
        :rtype: int
        :raises: ValueError if address is not a multiple of 4. RV32I instructions are 4 bytes wide.
                 IndexError if address is not a value index of the list of instructions.
        """
        if address % 4 != 0:
            raise ValueError(
                "Accessing invalid address of instruction! RV32I instructions are 4 bytes wide."
            )
        if address >= len(self.instructions) * 4:
            raise IndexError("Accessing out of bounds address in instruction memory!")
        self.inst_out = self.instructions[address // 4]
        return self.inst_out

    def fill_memory(self, encoded_instructions):
        """
        Fills the instruction memory (list) with the given encoded instructions (copies the list).

        :param encoded_instructions: encoded instructions
        :type encoded_instructions: list
        :return: None
        :rtype: NoneType
        """
        for i in range(len(encoded_instructions)):
            self.instructions[i] = encoded_instructions[i]
        self.fill_memory_bytes(encoded_instructions)

    def fill_memory_bytes(self, encoded_instructions):
        """
        Fills the list of instruction memory bytes with the instructions divided in four parts of 8 bits (byte).

        :param encoded_instructions: encoded instructions
        :type encoded_instructions: list
        :return: None
        :rtype: NoneType
        """
        # TODO: use list comprehension to make it clearer
        for i in range(len(encoded_instructions)):
            inst = encoded_instructions[i]
            self.instructions_bytes[i * 4] = mask_bits(inst, 0, 7)
            self.instructions_bytes[i * 4 + 1] = mask_bits(inst, 8, 15)
            self.instructions_bytes[i * 4 + 2] = mask_bits(inst, 16, 23)
            self.instructions_bytes[i * 4 + 3] = mask_bits(inst, 24, 31)

    def load_instructions_from_file(self, file):
        """
        Loads instructions from binary file.

        :param file: binary file containing instructions
        :type file: file
        :return: encoded instructions
        :rtype: list
        """
        try:
            with open(file, "rb") as f:
                encoded_instructions = f.readlines()
                encoded_instructions = [
                    int(inst.strip()) for inst in encoded_instructions
                ]
        except FileNotFoundError:
            print(f"Error: {file} not found")
            return
        except:
            print(f"Error: An error occurred while trying to read {file}")
            return
        self.fill_memory(encoded_instructions)
        return encoded_instructions

    def load_instructions_from_asm_file(self, file):
        """
        Loads instructions from RISC-V Assembly file.

        :param file: asm file containing instructions
        :type file: file
        :return: encoded instructions
        :rtype: list
        """
        encoded_instructions_file = write_file_encoded_instructions(file)
        return self.load_instructions_from_file(encoded_instructions_file)

    def print_instructions(self):
        """
        Prints all the instructions.

        :return: None
        :rtype: NoneType
        """
        for i in range(len(self.instructions)):
            print("Inst {:04X}: 0x{:08X}".format(i, self.fetch_instruction(i * 4)))

    def extend_memory(self, num_of_new_instructions):
        """
        Extends the instruction memory by a given amount of instructions.

        :param num_of_new_instructions: number of new instructions to extend
        :type num_of_new_instructions: int
        :return: None
        :rtype: NoneType
        """
        self.instructions.extend([0] * num_of_new_instructions)
