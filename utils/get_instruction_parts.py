import re


def get_instruction_parts(instruction):
    """
    This function takes an instruction as input, split it into its individual parts (operation and operands) and returns
    them as a list.

    Parameters:
    instruction (str): A string representing an assembly instruction.

    Returns:
    list: A list of the operation and operands of the instruction.
    """
    return [_ for _ in re.split('[(.*?) ,]', instruction) if _]
