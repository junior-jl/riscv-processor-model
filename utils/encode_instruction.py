from classes.InstructionType import InstructionType
from utils.get_instruction_parts import get_instruction_parts
from utils.get_type import get_type
from utils.mask_bits import mask_bits
from utils.sign_extend import sign_extend

registers = {
    'x0': 0,
    'zero': 0,
    'x1': 1,
    'ra': 1,
    'x2': 2,
    'sp': 2,
    'x3': 3,
    'gp': 3,
    'x4': 4,
    'tp': 4,
    'x5': 5,
    't0': 5,
    'x6': 6,
    't1': 6,
    'x7': 7,
    't2': 7,
    'x8': 8,
    's0': 8,
    'x9': 9,
    's1': 9,
    'x10': 10,
    'a0': 10,
    'x11': 11,
    'a1': 11,
    'x12': 12,
    'a2': 12,
    'x13': 13,
    'a3': 13,
    'x14': 14,
    'a4': 14,
    'x15': 15,
    'a5': 15,
    'x16': 16,
    'a6': 16,
    'x17': 17,
    'a7': 17,
    'x18': 18,
    's2': 18,
    'x19': 19,
    's3': 19,
    'x20': 20,
    's4': 20,
    'x21': 21,
    's5': 21,
    'x22': 22,
    's6': 22,
    'x23': 23,
    's7': 23,
    'x24': 24,
    's8': 24,
    'x25': 25,
    's9': 25,
    'x26': 26,
    's10': 26,
    'x27': 27,
    's11': 27,
    'x28': 28,
    't3': 28,
    'x29': 29,
    't4': 29,
    'x30': 30,
    't5': 30,
    'x31': 31,
    't6': 31,
}
f3 = {'add': 0x0,
      'sub': 0x0,
      'xor': 0x4,
      'or': 0x6,
      'and': 0x7,
      'sll': 0x1,
      'srl': 0x5,
      'sra': 0x5,
      'slt': 0x2,
      'sltu': 0x3,
      'addi': 0x0,
      'xori': 0x4,
      'ori': 0x6,
      'andi': 0x7,
      'slli': 0x1,
      'srli': 0x5,
      'srai': 0x5,
      'slti': 0x2,
      'sltiu': 0x3,
      'lb': 0x0,
      'lh': 0x1,
      'lw': 0x2,
      'lbu': 0x4,
      'lhu': 0x5,
      'sb': 0x0,
      'sh': 0x1,
      'sw': 0x2,
      'beq': 0x0,
      'bne': 0x1,
      'blt': 0x4,
      'bge': 0x5,
      'bltu': 0x6,
      'bgeu': 0x7,
      'jalr': 0x0}


def _encode_r(inst, mnemonic):
    # R-Type
    # funct7    rs2     rs1     funct3      rd      opcode
    #  (7)      (5)     (5)       (3)       (5)       (7)
    # opcode = 0110011 (0x33)
    rd = registers[inst[1]]
    rs1 = registers[inst[2]]
    rs2 = registers[inst[3]]
    opcode = 0x33
    funct3 = f3[mnemonic]
    funct7 = 0x20 if mnemonic in ['sub', 'sra'] else 0x0
    encoded_instruction = 0
    encoded_instruction |= (funct7 << (32 - 7))
    encoded_instruction |= (rs2 << (32 - 7 - 5))
    encoded_instruction |= (rs1 << (32 - 7 - 5 - 5))
    encoded_instruction |= (funct3 << (32 - 7 - 5 - 5 - 3))
    encoded_instruction |= (rd << (32 - 7 - 5 - 5 - 3 - 5))
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_i(inst, mnemonic):
    # I-Type
    # imm[11:0]    rs1     funct3      rd      opcode
    #    (12)      (5)       (3)       (5)       (7)
    # opcode = 0010011 (0x13) - arithmetics, 0000011 (0x03) - loads, 1100111 (0x67) - jalr
    rd = registers[inst[1]]
    rs1 = registers[inst[2]]
    imm = sign_extend(int(inst[3]), 12)
    if mnemonic == 'jalr':
        opcode = 0x67
    elif mnemonic in ['lb', 'lh', 'lw', 'lbu', 'lhu']:
        opcode = 0x03
    else:
        opcode = 0x13
    funct3 = f3[mnemonic]
    encoded_instruction = 0 if mnemonic != 'srai' else (1 << 30)
    encoded_instruction |= (imm << (32 - 12))
    encoded_instruction |= (rs1 << (32 - 12 - 5))
    encoded_instruction |= (funct3 << (32 - 12 - 5 - 3))
    encoded_instruction |= (rd << (32 - 12 - 5 - 3 - 5))
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_s(inst, mnemonic):
    # S-Type
    # imm[11:5]     rs2     rs1     funct3     imm[4:0]     opcode
    #   (7)         (5)     (5)       (3)         (5)        (7)
    # opcode = 0100011 (0x23)
    rs2 = registers[inst[1]]
    rs1 = registers[inst[2]]
    imm = sign_extend(int(inst[3]), 12)
    opcode = 0x23
    funct3 = f3[mnemonic]
    encoded_instruction = 0
    encoded_instruction |= ((mask_bits(imm, 5, 11)) << (32 - 7))
    encoded_instruction |= (rs2 << (32 - 7 - 5))
    encoded_instruction |= (rs1 << (32 - 7 - 5 - 5))
    encoded_instruction |= (funct3 << (32 - 7 - 5 - 5 - 3))
    encoded_instruction |= ((mask_bits(imm, 0, 4)) << (32 - 7 - 5 - 5 - 3 - 5))
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_u(inst, mnemonic):
    # U-Type
    # imm[31:12]     rd     opcode
    #    (20)        (5)      (7)
    # opcode = 0110111 (0x37) -> lui
    # opcode = 0010111 (0x17) -> auipc
    opcode = 0x37 if mnemonic == 'lui' else 0x17
    rd = registers[inst[1]]
    imm = sign_extend((int(inst[2])), 20)
    encoded_instruction = 0
    encoded_instruction |= (imm << (32 - 20))
    encoded_instruction |= (rd << (32 - 20 - 5))
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_sb(inst, mnemonic):
    # SB-Type
    # imm[12]   imm[10:5]   rs2     rs1     funct3      imm[4:1]    imm[11]     opcode
    #   (1)        (6)      (5)     (5)       (3)          (4)        (1)         (7)
    # opcode = 1100011 (0x63)
    opcode = 0x63
    rs1 = registers[inst[1]]
    rs2 = registers[inst[2]]
    imm = sign_extend((int(inst[3])), 13)
    funct3 = f3[mnemonic]
    encoded_instruction = 0
    encoded_instruction |= ((mask_bits(imm, 12, 12)) << (32 - 1))
    encoded_instruction |= ((mask_bits(imm, 5, 10)) << (32 - 1 - 6))
    encoded_instruction |= (rs2 << (32 - 1 - 6 - 5))
    encoded_instruction |= (rs1 << (32 - 1 - 6 - 5 - 5))
    encoded_instruction |= (funct3 << (32 - 1 - 6 - 5 - 5 - 3))
    encoded_instruction |= ((mask_bits(imm, 1, 4)) << (32 - 1 - 6 - 5 - 5 - 3 - 4))
    encoded_instruction |= ((mask_bits(imm, 11, 11)) << (32 - 1 - 6 - 5 - 5 - 3 - 4 - 1))
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def _encode_uj(inst, mnemonic):
    # UJ-Type
    # imm[20]   imm[10:1]   imm[11]     imm[19:12]    rd      opcode
    #   (1)        (10)       (1)           (8)       (5)       (7)
    # opcode = 1101111 (0x6F) -> jal
    opcode = 0x6F
    rd = registers[inst[1]]
    imm = sign_extend(int(inst[2]), 21)
    encoded_instruction = 0
    encoded_instruction |= ((mask_bits(imm, 20, 20)) << (32 - 1))
    encoded_instruction |= ((mask_bits(imm, 1, 10)) << (32 - 1 - 10))
    encoded_instruction |= ((mask_bits(imm, 11, 11)) << (32 - 1 - 10 - 1))
    encoded_instruction |= ((mask_bits(imm, 12, 19)) << (32 - 1 - 10 - 1 - 8))
    encoded_instruction |= (rd << (32 - 1 - 10 - 1 - 8 - 5))
    encoded_instruction |= opcode
    encoded_instruction = mask_bits(encoded_instruction, 0, 31)
    return encoded_instruction


def encode_instruction(instruction):
    instruction = get_instruction_parts(instruction)
    inst_type, inst_operation = get_type(instruction)
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
    else:
        raise ValueError("Invalid type of instruction")

