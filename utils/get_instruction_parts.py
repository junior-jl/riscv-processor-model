import re


def get_instruction_parts(instruction):
    """
    This function takes an instruction as input, split it into its individual parts (operation and operands) and returns
    them as a list.

    :param instruction: The instruction to be split
    :type instruction: str
    :return: The instruction divided into parts
    :rtype: list
    """
    return [_ for _ in re.split("[(.*?) ,]", instruction) if _]
