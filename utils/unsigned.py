def unsigned(num):
    """
    Converts a signed integer to an unsigned integer.

    :param num: The signed integer to be converted
    :type num: int
    :return: The unsigned representation of the given signed integer
    :rtype: int
    """
    return num + (1 << 32) if num < 0 else num
