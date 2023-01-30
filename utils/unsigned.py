def unsigned(num):
    return num + (1 << 32) if num < 0 else num
