def get_instructions_asm_file(file):
    """
    This function reads the assembly code from a file and stores each instruction as an element of a list.

    :param file: The file containing the Assembly instructions
    :type file: file
    :return: A tuple containing the instructions on the file
    :rtype: tuple
    :raises: FileNotFoundError if the file does not exist
    """
    instructions = []
    try:
        f = open(file, "r")
    except FileNotFoundError:
        raise FileNotFoundError("File not found")
    else:
        with f:
            for line in f:
                # Allow one-line comments and ignore blank lines
                if line != "\n" and line[0] != "#":
                    # Remove the newlines
                    instructions.append(line.rstrip())
    return tuple(instructions)
