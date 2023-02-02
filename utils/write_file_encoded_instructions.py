from utils.encode_instructions import encode_instructions
from utils.get_instructions_asm_file import get_instructions_asm_file


def write_file(info, file):
    """
    Writes a list of elements to a file.

    :param info: List of elements to be written to the file.
    :type info: list
    :param file: File path to write to
    :type file: str
    :return: None
    :rtype: NoneType
    """
    with open(file, "w") as f:
        for item in info:
            f.write(str(item) + "\n")


def write_file_encoded_instructions(file):
    """
    Generates a file with the encoded instructions from an assembly file.

    :param file: Assembly file path.
    :type file: str
    :return: Name of the generated file with the encoded instructions.
    :rtype: str
    """
    file_name = file
    new_file = file_name.split(".")[0]
    asm = get_instructions_asm_file(file)
    code = encode_instructions(asm)
    write_file(code, new_file)
    return new_file
