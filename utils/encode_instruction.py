from classes.InstructionType import InstructionType
from utils.get_instruction_parts import get_instruction_parts
from utils.get_type import get_type
from utils.mask_bits import mask_bits
from utils.sign_extend import sign_extend

registers = {
    "x0": 0,
    "zero": 0,
    "x1": 1,
    "ra": 1,
    "x2": 2,
    "sp": 2,
    "x3": 3,
    "gp": 3,
    "x4": 4,
    "tp": 4,
    "x5": 5,
    "t0": 5,
    "x6": 6,
    "t1": 6,
    "x7": 7,
    "t2": 7,
    "x8": 8,
    "s0": 8,
    "x9": 9,
    "s1": 9,
    "x10": 10,
    "a0": 10,
    "x11": 11,
    "a1": 11,
    "x12": 12,
    "a2": 12,
    "x13": 13,
    "a3": 13,
    "x14": 14,
    "a4": 14,
    "x15": 15,
    "a5": 15,
    "x16": 16,
    "a6": 16,
    "x17": 17,
    "a7": 17,
    "x18": 18,
    "s2": 18,
    "x19": 19,
    "s3": 19,
    "x20": 20,
    "s4": 20,
    "x21": 21,
    "s5": 21,
    "x22": 22,
    "s6": 22,
    "x23": 23,
    "s7": 23,
    "x24": 24,
    "s8": 24,
    "x25": 25,
    "s9": 25,
    "x26": 26,
    "s10": 26,
    "x27": 27,
    "s11": 27,
    "x28": 28,
    "t3": 28,
    "x29": 29,
    "t4": 29,
    "x30": 30,
    "t5": 30,
    "x31": 31,
    "t6": 31,
}
f3 = {
    "add": 0x0,
    "sub": 0x0,
    "xor": 0x4,
    "or": 0x6,
    "and": 0x7,
    "sll": 0x1,
    "srl": 0x5,
    "sra": 0x5,
    "slt": 0x2,
    "sltu": 0x3,
    "addi": 0x0,
    "xori": 0x4,
    "ori": 0x6,
    "andi": 0x7,
    "slli": 0x1,
    "srli": 0x5,
    "srai": 0x5,
    "slti": 0x2,
    "sltiu": 0x3,
    "lb": 0x0,
    "lh": 0x1,
    "lw": 0x2,
    "lbu": 0x4,
    "lhu": 0x5,
    "sb": 0x0,
    "sh": 0x1,
    "sw": 0x2,
    "beq": 0x0,
    "bne": 0x1,
    "blt": 0x4,
    "bge": 0x5,
    "bltu": 0x6,
    "bgeu": 0x7,
    "jalr": 0x0,
}


# TODO: Refactor


def _encode_r(inst, mnemonic):
    """
    Encode R-Type instruction into 32-bit machine code.

    # R-Type
    # funct7    rs2     rs1     funct3      rd      opcode
    #  (7)      (5)     (5)       (3)       (5)       (7)
    # opcode = 0110011 (0x33)

    :param inst: A list of strings that represents the instruction and its operands
    :type inst: list
    :param mnemonic: The string containing the mnemonic of the instruction
    :type mnemonic: str
    :return: The encoded instruction in 32-bit format
    :rtype: int
    """
    rd = registers[inst[1]]
    rs1 = registers[inst[2]]
    rs2 = registers[inst[3]]
    opcode = 0x33
    funct3 = f3[mnemonic]
    funct7 = 0x20 if mnemonic in ["sub", "sra"] else 0x0
    encoded_instruction = 0
    encoded_instruction |= funct7 << (32 - 7)
    encoded_instruction |= rs2 << (32 - 7 - 5)
    encoded_instruction |= rs1 << (32 - 7 - 5 - 5)
    encoded_instruction |= funct3 << (32 - 7 - 5 - 5 - 3)
    encoded_instruction |= rd << (32 - 7 - 5 - 5 - 3 - 5)
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_i(inst, mnemonic):
    """
    Encode I-Type instruction into 32-bit machine code.

    # I-Type
    # imm[11:0]    rs1     funct3      rd      opcode
    #    (12)      (5)       (3)       (5)       (7)
    # opcode = 0010011 (0x13) - arithmetics, 0000011 (0x03) - loads, 1100111 (0x67) - jalr

    :param inst: A list of strings that represents the instruction and its operands
    :type inst: list
    :param mnemonic: The string containing the mnemonic of the instruction
    :type mnemonic: str
    :return: The encoded instruction in 32-bit format
    :rtype: int
    """
    rd = registers[inst[1]]
    if inst[2] in registers.keys():
        rs1 = registers[inst[2]]
        imm = inst[3]
    else:
        rs1 = registers[inst[3]]
        imm = inst[2]
    if imm[0:2] in ["0x", "0X"]:
        imm = int(imm[2:], 16)
    elif imm[0:2] in ["0b", "0B"]:
        imm = int(imm[2:], 2)
    else:
        imm = int(imm)
    imm = sign_extend(imm, 12)
    if mnemonic == "jalr":
        opcode = 0x67
    elif mnemonic in ["lb", "lh", "lw", "lbu", "lhu"]:
        opcode = 0x03
    else:
        opcode = 0x13
    funct3 = f3[mnemonic]
    encoded_instruction = 0 if mnemonic != "srai" else (1 << 30)
    encoded_instruction |= imm << (32 - 12)
    encoded_instruction |= rs1 << (32 - 12 - 5)
    encoded_instruction |= funct3 << (32 - 12 - 5 - 3)
    encoded_instruction |= rd << (32 - 12 - 5 - 3 - 5)
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_s(inst, mnemonic):
    """
    Encode S-Type instruction into 32-bit machine code.

    # S-Type
    # imm[11:5]     rs2     rs1     funct3     imm[4:0]     opcode
    #   (7)         (5)     (5)       (3)         (5)        (7)
    # opcode = 0100011 (0x23)

    :param inst: A list of strings that represents the instruction and its operands
    :type inst: list
    :param mnemonic: The string containing the mnemonic of the instruction
    :type mnemonic: str
    :return: The encoded instruction in 32-bit format
    :rtype: int
    """
    rs2 = registers[inst[1]]
    if inst[2] in registers.keys():
        rs1 = registers[inst[2]]
        imm = inst[3]
    else:
        rs1 = registers[inst[3]]
        imm = inst[2]
    if imm[0:2] in ["0x", "0X"]:
        imm = int(imm[2:], 16)
    elif imm[0:2] in ["0b", "0B"]:
        imm = int(imm[2:], 2)
    else:
        imm = int(imm)
    imm = sign_extend(imm, 12)
    opcode = 0x23
    funct3 = f3[mnemonic]
    encoded_instruction = 0
    encoded_instruction |= (mask_bits(imm, 5, 11)) << (32 - 7)
    encoded_instruction |= rs2 << (32 - 7 - 5)
    encoded_instruction |= rs1 << (32 - 7 - 5 - 5)
    encoded_instruction |= funct3 << (32 - 7 - 5 - 5 - 3)
    encoded_instruction |= (mask_bits(imm, 0, 4)) << (32 - 7 - 5 - 5 - 3 - 5)
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_u(inst, mnemonic):
    """
    Encode U-Type instruction into 32-bit machine code.

    # U-Type
    # imm[31:12]     rd     opcode
    #    (20)        (5)      (7)
    # opcode = 0110111 (0x37) -> lui
    # opcode = 0010111 (0x17) -> auipc

    :param inst: A list of strings that represents the instruction and its operands
    :type inst: list
    :param mnemonic: The string containing the mnemonic of the instruction
    :type mnemonic: str
    :return: The encoded instruction in 32-bit format
    :rtype: int
    """
    opcode = 0x37 if mnemonic == "lui" else 0x17
    rd = registers[inst[1]]
    if inst[2][0:2] in ["0x", "0X"]:
        imm = int(inst[2][2:], 16)
    elif inst[2][0:2] in ["0b", "0B"]:
        imm = int(inst[2][2:], 2)
    else:
        imm = int(inst[2])
    encoded_instruction = 0
    encoded_instruction |= imm << (32 - 20)
    encoded_instruction |= rd << (32 - 20 - 5)
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_sb(inst, mnemonic):
    """
    Encode SB-Type instruction into 32-bit machine code.

    # SB-Type
    # imm[12]   imm[10:5]   rs2     rs1     funct3      imm[4:1]    imm[11]     opcode
    #   (1)        (6)      (5)     (5)       (3)          (4)        (1)         (7)
    # opcode = 1100011 (0x63)

    :param inst: A list of strings that represents the instruction and its operands
    :type inst: list
    :param mnemonic: The string containing the mnemonic of the instruction
    :type mnemonic: str
    :return: The encoded instruction in 32-bit format
    :rtype: int
    """
    opcode = 0x63
    rs1 = registers[inst[1]]
    rs2 = registers[inst[2]]
    if inst[3][0:2] in ["0x", "0X"]:
        imm = int(inst[3][2:], 16)
    elif inst[3][0:2] in ["0b", "0B"]:
        imm = int(inst[3][2:], 2)
    else:
        imm = int(inst[3])
    imm = sign_extend(imm, 13)
    funct3 = f3[mnemonic]
    encoded_instruction = 0
    encoded_instruction |= (mask_bits(imm, 12, 12)) << (32 - 1)
    encoded_instruction |= (mask_bits(imm, 5, 10)) << (32 - 1 - 6)
    encoded_instruction |= rs2 << (32 - 1 - 6 - 5)
    encoded_instruction |= rs1 << (32 - 1 - 6 - 5 - 5)
    encoded_instruction |= funct3 << (32 - 1 - 6 - 5 - 5 - 3)
    encoded_instruction |= (mask_bits(imm, 1, 4)) << (32 - 1 - 6 - 5 - 5 - 3 - 4)
    encoded_instruction |= (mask_bits(imm, 11, 11)) << (32 - 1 - 6 - 5 - 5 - 3 - 4 - 1)
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_uj(inst, mnemonic):
    """
    Encode UJ-Type instruction into 32-bit machine code.

    # UJ-Type
    # imm[20]   imm[10:1]   imm[11]     imm[19:12]    rd      opcode
    #   (1)        (10)       (1)           (8)       (5)       (7)
    # opcode = 1101111 (0x6F) -> jal

    :param inst: A list of strings that represents the instruction and its operands
    :type inst: list
    :param mnemonic: The string containing the mnemonic of the instruction
    :type mnemonic: str
    :return: The encoded instruction in 32-bit format
    :rtype: int
    """
    # TODO: Mnemonic unused, refactor!
    # TODO: Add option to write 'jal offset' meaning 'jal ra, offset'
    opcode = 0x6F
    rd = registers[inst[1]]
    if inst[2][0:2] in ["0x", "0X"]:
        imm = int(inst[2][2:], 16)
    elif inst[2][0:2] in ["0b", "0B"]:
        imm = int(inst[2][2:], 2)
    else:
        imm = int(inst[2])
    imm = sign_extend(imm, 21)
    encoded_instruction = 0
    encoded_instruction |= (mask_bits(imm, 20, 20)) << (32 - 1)
    encoded_instruction |= (mask_bits(imm, 1, 10)) << (32 - 1 - 10)
    encoded_instruction |= (mask_bits(imm, 11, 11)) << (32 - 1 - 10 - 1)
    encoded_instruction |= (mask_bits(imm, 12, 19)) << (32 - 1 - 10 - 1 - 8)
    encoded_instruction |= rd << (32 - 1 - 10 - 1 - 8 - 5)
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_pseudo(inst, mnemonic):
    if mnemonic == "nop":
        return _encode_i(["addi", "x0", "x0", "0"], "addi")
    elif mnemonic == "li":
        rd = inst[1]
        imm = inst[2]
        return _encode_i(["addi", rd, "x0", imm], "addi")
    elif mnemonic == "mv":
        rd = inst[1]
        rs = inst[2]
        return _encode_i(["addi", rd, rs, "0"], "addi")
    elif mnemonic == "not":
        rd = inst[1]
        rs = inst[2]
        return _encode_i(["xori", rd, rs, "-1"], "xori")
    elif mnemonic == "neg":
        rd = inst[1]
        rs = inst[2]
        return _encode_r(["sub", rd, "x0", rs], "sub")
    elif mnemonic == "beqz":
        rs = inst[1]
        offset = inst[2]
        return _encode_sb(["beq", rs, "x0", offset], "beq")
    elif mnemonic == "bnez":
        rs = inst[1]
        offset = inst[2]
        return _encode_sb(["bne", rs, "x0", offset], "bne")
    elif mnemonic == "j":
        offset = inst[1]
        return _encode_uj(["jal", "x0", offset], "jal")
    elif mnemonic == "jr":
        rs = inst[1]
        return _encode_i(["jalr", "x0", rs, "0"], "jalr")
    elif mnemonic == "ret":
        return _encode_i(["jalr", "x0", "x1", "0"], "jalr")
    else:
        raise ValueError(f"Invalid mnemonic ({mnemonic})!")


def encode_instruction(instruction):
    """
    Encode a RISC-V Assembly instruction into 32-bit machine code based on its type.

    :param instruction: The Assembly instruction to be encoded into machine code
    :type instruction: str
    :return: The encoded instruction
    :rtype: int
    :raises: ValueError if the type of instruction is not valid for RV32I
    """
    instruction = get_instruction_parts(instruction)
    inst_type, inst_operation = get_type(instruction)
    # TODO: Refactor | To get comments working in pseudoinstructions, maybe call this function again after
    #  'translating' it
    if inst_type in [
        InstructionType.R,
        InstructionType.I,
        InstructionType.S,
        InstructionType.SB,
    ]:
        if len(instruction) > 4 and instruction[4][0] != "#":
            raise ValueError("Comments should start with the # sign!")
    else:
        if len(instruction) > 3 and instruction[3][0] != "#":
            raise ValueError("Comments should start with the # sign!")
    if inst_type == InstructionType.R:
        return _encode_r(instruction, inst_operation)
    elif inst_type == InstructionType.I:
        return _encode_i(instruction, inst_operation)
    elif inst_type == InstructionType.S:
        return _encode_s(instruction, inst_operation)
    elif inst_type == InstructionType.U:
        return _encode_u(instruction, inst_operation)
    elif inst_type == InstructionType.SB:
        return _encode_sb(instruction, inst_operation)
    elif inst_type == InstructionType.UJ:
        return _encode_uj(instruction, inst_operation)
    elif inst_type == InstructionType.PSEUDO:
        return _encode_pseudo(instruction, inst_operation)
    else:
        raise ValueError(f"Invalid type of instruction ({inst_type})!")
