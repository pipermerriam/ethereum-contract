from sha3 import sha3_256


def strip_0x_prefix(value):
    if value.startswith('0x'):
        return value[2:]
    return value


def clean_args(*args):
    for _type, arg in args:
        if _type == 'address':
            yield strip_0x_prefix(arg)
        else:
            yield arg


def sha3(seed):
    return sha3_256(seed).digest()
