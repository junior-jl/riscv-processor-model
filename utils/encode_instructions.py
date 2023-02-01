from utils.encode_instruction import encode_instruction
from utils.get_instructions_asm_file import get_instructions_asm_file


def encode_instructions(asm_instructions):
    return list(map(encode_instruction, asm_instructions))


def encode_instructions_from_file(file):
    asm_instructions = get_instructions_asm_file(file)
    return encode_instructions(asm_instructions)


def print_encoded_instructions(encoded_instructions, representation):
    if representation == "hex":
        for i in range(len(encoded_instructions)):
            print("0x{:X}:\t0x{:08X}".format(i * 4, encoded_instructions[i]))
