import sys
from sha3 import sha3_256


if sys.version_info.major == 2:
    str_to_bytes = str
else:
    def str_to_bytes(value):
        if isinstance(value, bytearray):
            value = bytes(value)
        if isinstance(value, bytes):
            return value
        return bytes(value, 'utf-8')


def strip_0x_prefix(value):
    if value.startswith(b'0x'):
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
