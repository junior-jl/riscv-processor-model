from utils.mask_bits import mask_bits


def sign_extend(num, bits=32, sign=None, size=12):
    if bits <= 0:
        raise ValueError("Number of bits must be greater than 0")
    mask = ((1 << bits) - 1) << size if sign == 1 else 0
    mask = mask_bits(mask, size, bits-1) << size
    return num | mask
