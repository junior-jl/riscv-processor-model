from utils.encode_instruction import encode_instruction
from utils.encode_instructions import encode_instructions_from_file, print_encoded_instructions

# 1. Instruction Fetch
# 2. Instruction Decode
# 3. Execute
# 4. Memory
# 5. Write Back
# TODO: Accept format with parenthesis
if __name__ == '__main__':
    code = encode_instructions_from_file('teste.s')
    print_encoded_instructions(code, 'hex')
