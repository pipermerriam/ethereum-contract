import sys
from sha3 import sha3_256


if sys.version_info.major == 2:
    str_to_bytes = str
    int_types = (int, long)  # NOQA `long` not defined in py3
    text_types = (basestring,)  # NOQA `basestr` not defined in py3
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


def get_contract_name_from_source(contract_source):
    left = contract_source.index('contract') + len('contract')
    right = contract_source.index('{')

    if left < right:
        contract_name = contract_source[left:right].strip()
    else:
        raise ValueError("Could not find a contract name in the provided source")

    return contract_name


def construct_contract_docstring(contract_name,
                                 constructor_sig,
                                 function_sigs,
                                 event_sigs):
    # Construct the components that will make up the docstring for the
    # contract.
    if constructor_sig:
        constructor_docstring = '// Constructor\n' + constructor_sig + ';'
    else:
        constructor_docstring = ''

    if event_sigs:
        events_docstring = '// Events\n' + (
            '\n'.join(sig + ';' for sig in event_sigs)
        )
    else:
        events_docstring = ''

    if function_sigs:
        functions_docstring = '// Functions\n' + (
            '\n'.join(sig + ';' for sig in function_sigs)
        )
    else:
        functions_docstring = ''

    docstring_body = '\n\n'.join([
        constructor_docstring,
        events_docstring,
        functions_docstring,
    ])

    docstring = """
    contract {contract_name} {{
    {{body}}
    }}
    """.format(
        contract_name=contract_name,
        body=docstring_body,
    )
    return docstring
