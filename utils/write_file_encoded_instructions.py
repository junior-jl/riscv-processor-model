from utils.encode_instructions import encode_instructions
from utils.get_instructions_asm_file import get_instructions_asm_file


def write_file(info, file):
    with open(file, "w") as f:
        for item in info:
            f.write(str(item) + "\n")


def write_file_encoded_instructions(file):
    file_name = file
    new_file = file_name.split(".")[0]
    asm = get_instructions_asm_file(file)
    code = encode_instructions(asm)
    # new_file = f'{new_file}.txt'
    write_file(code, new_file)
    return new_file
