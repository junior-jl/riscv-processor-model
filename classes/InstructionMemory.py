from utils.encode_instructions import encode_instructions
from utils.get_instructions_asm_file import get_instructions_asm_file
from utils.mask_bits import mask_bits
from utils.write_file_encoded_instructions import write_file_encoded_instructions


class InstructionMemory:
    def __init__(self, words=32, encoded_instructions=None):
        self.inst_out = None
        if not encoded_instructions:
            self.instructions = [0] * words
            self.instructions_bytes = [0] * words * 4
        else:
            self.instructions = [0] * len(encoded_instructions)
            self.instructions_bytes = [0] * 4 * len(encoded_instructions)
            self.fill_memory(encoded_instructions)

    def fetch_instruction(self, address):
        if address % 4 != 0:
            raise ValueError('Accessing invalid address of instruction! RV32I instructions are 4 bytes wide.')
        if address >= len(self.instructions) * 4:
            raise IndexError('Accessing out of bounds address in instruction memory!')
        self.inst_out = self.instructions[address // 4]
        return self.inst_out

    def fill_memory(self, encoded_instructions):
        for i in range(len(encoded_instructions)):
            self.instructions[i] = encoded_instructions[i]
        self.fill_memory_bytes(encoded_instructions)

    def fill_memory_bytes(self, encoded_instructions):
        # TODO: use list comprehension to make it clearer
        for i in range(len(encoded_instructions)):
            inst = encoded_instructions[i]
            self.instructions_bytes[i * 4] = mask_bits(inst, 0, 7)
            self.instructions_bytes[i * 4 + 1] = mask_bits(inst, 8, 15)
            self.instructions_bytes[i * 4 + 2] = mask_bits(inst, 16, 23)
            self.instructions_bytes[i * 4 + 3] = mask_bits(inst, 24, 31)

    def load_instructions_from_file(self, file):
        try:
            with open(file, 'rb') as f:
                encoded_instructions = f.readlines()
                encoded_instructions = [int(inst.strip()) for inst in encoded_instructions]
        except FileNotFoundError:
            print(f'Error: {file} not found')
            return
        except:
            print(f'Error: An error occurred while trying to read {file}')
            return
        self.fill_memory(encoded_instructions)

    def load_instructions_from_asm_file(self, file):
        encoded_instructions_file = write_file_encoded_instructions(file)
        self.load_instructions_from_file(encoded_instructions_file)

    def print_instructions(self):
        for i in range(len(self.instructions)):
            print('Inst {:04X}: 0x{:08X}'.format(i, self.fetch_instruction(i * 4)))

    def extend_memory(self, num_of_new_instructions):
        self.instructions.extend([0] * num_of_new_instructions)


write_file_encoded_instructions('teste.s')
