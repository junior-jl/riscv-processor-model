def mask_bits(num, start, end):
    """
    Masks the specified bits from the given number.

    :param num: The number from which to extract the bits
    :type num: int
    :param start: The starting bit to be extracted (0-indexed)
    :type start: int
    :param end: The ending bit to be extracted (0-indexed)
    :type end: int
    :return: The extracted bits as a binary integer
    :rtype: int
    """
    mask = (1 << (end - start + 1)) - 1
    return (num >> start) & mask
