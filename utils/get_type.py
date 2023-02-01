from classes.InstructionType import InstructionType
from utils.get_instruction_parts import get_instruction_parts


def get_type(inst):
    """
    This function takes an instruction as input and returns its operation and type according to the RISC-V
    instruction set. The instruction type can be R, I, S, U, SB or UJ.

    Parameters:
    inst (list[str]): A list containing the parts of a RISC-V assembly instruction.

    Returns:
    Tuple[InstructionType, str]: A tuple containing the instruction operation and its type.

    Raises:
    ValueError: If the instruction is not valid.
    """
    operation = inst[0]
    # R-Type
    if operation.lower() in [
        "add",
        "and",
        "or",
        "slt",
        "sltu",
        "sll",
        "srl",
        "sra",
        "sub",
        "xor",
    ]:
        type = InstructionType.R
    # I-Type
    elif operation.lower() in [
        "addi",
        "andi",
        "jalr",
        "lb",
        "lbu",
        "lhu",
        "lh",
        "lw",
        "ori",
        "slti",
        "sltiu",
        "slli",
        "srai",
        "srli",
        "xori",
    ]:
        type = InstructionType.I
    # S-Type
    elif operation.lower() in ["sb", "sh", "sw"]:
        type = InstructionType.S
    # U-Type
    elif operation.lower() in ["auipc", "lui"]:
        type = InstructionType.U
    # SB-Type
    elif operation.lower() in ["beq", "bge", "bgeu", "blt", "bltu", "bne"]:
        type = InstructionType.SB
    # UJ-Type
    elif operation.lower() == "jal":
        type = InstructionType.UJ
    else:
        raise ValueError("Invalid instruction!")
    return type, operation
