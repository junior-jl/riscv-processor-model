from enum import Enum


class InstructionType(Enum):
    """
    The InstructionType Enum class defines the different types of instructions that are supported in the RISC-V ISA.
    """

    R = "R"
    I = "I"
    S = "S"
    U = "U"
    SB = "SB"
    UJ = "UJ"
