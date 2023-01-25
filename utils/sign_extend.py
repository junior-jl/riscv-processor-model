def sign_extend(num, bits):
    if bits <= 0:
        raise ValueError("Number of bits must be greater than 0")
    sign_bit = (num < 0) << (bits - 1)
    mask = (1 << bits) - 1
    return (num & mask) | ((-num & sign_bit) << 1)
