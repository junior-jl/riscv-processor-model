from utils.mask_bits import mask_bits


class InstructionMemory:
    def __init__(self, words, encoded_instructions=None):
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
        return self.instructions[address // 4]

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
                encoded_instructions = f.read()
        except FileNotFoundError:
            print(f'Error: {file} not found')
            return
        except:
            print(f'Error: An error occurred while trying to read {file}')
            return
        self.fill_memory(encoded_instructions)

    def print_instructions(self):
        print(self.instructions)

    def extend_memory(self, num_of_new_instructions):
        self.instructions.extend([0] * num_of_new_instructions)
