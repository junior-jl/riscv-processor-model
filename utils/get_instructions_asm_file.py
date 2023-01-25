def get_instructions_asm_file(file):
    """
    This function reads the assembly code from a file and stores each instruction as an element of a list.

    Parameters:
    file (str): The file containing the assembly code.

    Returns:
    tuple: A tuple containing the assembly instructions.
    """
    instructions = []
    try:
        f = open(file, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    else:
        with f:
            for line in f:
                # Remove the newlines
                instructions.append(line.rstrip())
    return tuple(instructions)
