from utils.mask_bits import mask_bits


def get_bit_size(num, bits=32):
    while not (num & (1 << (bits - 1))):
        bits -= 1
    return bits


def sign_extend(num, bits=32, sign=None, size=12):
    sign = (num >> (size - 1)) & 1 if not sign else sign
    if bits <= 0:
        raise ValueError("Number of bits must be greater than 0")
    mask = ((1 << bits) - 1) << size if sign == 1 else 0
    mask = mask_bits(mask, size, bits - 1) << size
    return num | mask
