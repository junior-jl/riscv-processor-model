from utils.mask_bits import mask_bits


def get_bit_size(num, bits=32):
    """
    Given a number, returns the number of bits necessary to represent it.

    :param num: The number for which to determine the number of bits necessary for representing it
    :type num: int
    :param bits: The maximum bits for representation (default: 32)
    :type bits: int, optional
    :return: The number of bits needed to represent the number
    :rtype: int
    """
    while not (num & (1 << (bits - 1))):
        bits -= 1
    return bits


def sign_extend(num, bits=32, sign=None, size=12):
    """
    Sign extends a given number, returning a number with the specified number of bits.

    :param num: The number to sign extend.
    :type num: int
    :param bits: The number of bits in the sign-extended result (default: 32).
    :type bits: int, optional
    :param sign: The sign to extend. If not provided, it will be computed from the input number (default: None).
    :type sign: int, optional
    :param size: The number of bits in the input number (default: 12).
    :type size: int, optional
    :return: The sign-extended number.
    :rtype: int
    """
    sign = (num >> (size - 1)) & 1 if not sign else sign
    if bits <= 0:
        raise ValueError("Number of bits must be greater than 0")
    mask = ((1 << bits) - 1) << size if sign == 1 else 0
    mask = mask_bits(mask, size, bits - 1) << size
    return num | mask
