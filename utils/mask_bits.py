def mask_bits(num, start, end):
    mask = (1 << (end - start + 1)) - 1
    return (num >> start) & mask
