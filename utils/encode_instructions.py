from utils.encode_instruction import encode_instruction
from utils.get_instructions_asm_file import get_instructions_asm_file


def encode_instructions(asm_instructions):
    """
    Encodes a list of RISC-V Assembly instructions into their binary representation.

    :param asm_instructions: Tuple of Assembly instructions
    :type asm_instructions: tuple
    :return: List of encoded instructions
    :rtype: list
    """
    return list(map(encode_instruction, asm_instructions))


def encode_instructions_from_file(file):
    """
    Encodes Assembly instructions from a file into their binary representation.

    :param file: The file containing the Assembly instructions
    :type file: file
    :return: List of encoded instructions
    :rtype: list
    """
    asm_instructions = get_instructions_asm_file(file)
    return encode_instructions(asm_instructions)


def print_encoded_instructions(encoded_instructions, representation):
    """
    Prints the encoded binary instructions in the specified representation.

    :param encoded_instructions: List of encoded binary instructions
    :type encoded_instructions: list
    :param representation: Representation format for the binary instructions (either 'hex', 'bin' or 'dec')
    :type representation: str
    :raises: ValueError if invalid representation
    """
    if representation == "hex":
        for i in range(len(encoded_instructions)):
            print("0x{:X}:\t0x{:08X}".format(i * 4, encoded_instructions[i]))
    elif representation == "bin":
        for i in range(len(encoded_instructions)):
            print("0x{:X}:\t0x{:064b}".format(i * 4, encoded_instructions[i]))
    elif representation == "dec":
        for i in range(len(encoded_instructions)):
            print("0x{:X}:\t0x{:d}".format(i * 4, encoded_instructions[i]))
    else:
        raise ValueError(
            f'Invalid representation: {representation}. Allowed values are: "hex", "bin" or "dec".'
        )
