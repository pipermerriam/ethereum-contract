import sys
from sha3 import sha3_256


if sys.version_info.major == 2:
    str_to_bytes = str
    int_types = (int, long)
    text_types = (basestring,)
else:
    def str_to_bytes(value):
        if isinstance(value, bytearray):
            value = bytes(value)
        if isinstance(value, bytes):
            return value
        return bytes(value, 'utf-8')

    int_types = (int,)
    text_types = (bytes, str)


def strip_0x_prefix(value):
    if value.startswith(b'0x'):
        return value[2:]
    return value


def clean_args(*args):
    for _type, arg in args:
        if isinstance(arg, text_types):
            arg = str_to_bytes(arg)

        if _type == 'address':
            arg = strip_0x_prefix(arg)

        yield arg


def sha3(seed):
    return sha3_256(seed).digest()
