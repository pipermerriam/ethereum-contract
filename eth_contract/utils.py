import sys
import functools

from sha3 import sha3_256


if sys.version_info.major == 2:
    integer_types = (int, long)   # NOQA
    bytes_types = (bytes, bytearray)
    text_types = (unicode,)  # NOQA
    string_types = (basestring, bytearray)  # NOQA
else:
    integer_types = (int,)
    bytes_types = (bytes, bytearray)
    text_types = (str,)
    string_types = (bytes, str, bytearray)


def is_integer(value):
    return isinstance(value, integer_types)


def is_bytes(value):
    return isinstance(value, bytes_types)


def is_text(value):
    return isinstance(value, text_types)


def is_string(value):
    return isinstance(value, string_types)


if sys.version_info.major == 2:
    def force_bytes(value):
        if is_bytes(value):
            return str(value)
        elif is_text(value):
            return value.encode('latin1')
        else:
            raise TypeError("Unsupported type: {0}".format(type(value)))

    def force_text(value):
        if is_text(value):
            return value
        elif is_bytes(value):
            return unicode(force_bytes(value), 'latin1')  # NOQA
        else:
            raise TypeError("Unsupported type: {0}".format(type(value)))
else:
    def force_bytes(value):
        if is_bytes(value):
            return bytes(value)
        elif is_text(value):
            return bytes(value, 'latin1')
        else:
            raise TypeError("Unsupported type: {0}".format(type(value)))

    def force_text(value):
        if isinstance(value, text_types):
            return value
        elif isinstance(value, bytes_types):
            return str(value, 'latin1')
        else:
            raise TypeError("Unsupported type: {0}".format(type(value)))


def force_obj_to_bytes(obj):
    if is_string(obj):
        return force_bytes(obj)
    elif isinstance(obj, dict):
        return {
            k: force_obj_to_bytes(v) for k, v in obj.items()
        }
    elif isinstance(obj, (list, tuple)):
        return type(obj)(force_obj_to_bytes(v) for v in obj)
    else:
        return obj


def force_obj_to_text(obj):
    if is_string(obj):
        return force_text(obj)
    elif isinstance(obj, dict):
        return {
            k: force_obj_to_text(v) for k, v in obj.items()
        }
    elif isinstance(obj, (list, tuple)):
        return type(obj)(force_obj_to_text(v) for v in obj)
    else:
        return obj


def coerce_args_to_bytes(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        bytes_args = force_obj_to_bytes(args)
        bytes_kwargs = force_obj_to_bytes(kwargs)
        return fn(*bytes_args, **bytes_kwargs)
    return inner


def coerce_return_to_bytes(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        return force_obj_to_bytes(fn(*args, **kwargs))
    return inner


@coerce_args_to_bytes
def remove_0x_prefix(value):
    if value.startswith(b'0x'):
        return value[2:]
    return value


@coerce_args_to_bytes
def add_0x_prefix(value):
    return b"0x" + remove_0x_prefix(value)


def sha3(seed):
    return sha3_256(seed).digest()
