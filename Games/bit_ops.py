def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


def check_bit(x, n):
    return x & (1 << n)


def combine(a, b):
    return a | b
