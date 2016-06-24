import collections

from rlp.utils import (
    encode_hex,
)

from eth_contract.functions import (
    Function,
    FunctionGroup,
)
from eth_contract.events import Event
from eth_contract.utils import (
    str_to_bytes,
)


class ContractBase(object):
    # instance level variables
    address = None

    # class level variables
    name = None
    constructor = None
    events = None
    functions = None
    code = None
    runtime = None
    source = None

    def __init__(self, address, blockchain_client):
        self.blockchain_client = blockchain_client
        self.address = address

    def __str__(self):
        return str(self.name if self.name else "Unknown")

    @classmethod
    def deploy(cls):
        raise NotImplementedError("TODO")

    @classmethod
    def encodeABI(cls, fn, fn_args):
        """
        Return the ABI encoded call data for the provided function.
        """
        raise NotImplementedError("TODO")

    def on(self, *args, **kwargs):
        """
        Register a callback to be called whenever an event occurs.
        """
        raise NotImplementedError("TODO")

    def pastEvents(self, *args, **kwargs):
        """
        Register a callback to be called on all past occurrances of an event.
        """
        raise NotImplementedError("TODO")

    #
    # def tx_data(cls, sender=None, to, gas, gasPrice, value, data):
    #

    @classmethod
    def estimateGas(cls, *args, **kwargs):
        raise NotImplementedError("TODO")

    def call(self, *args, **kwargs):
        raise NotImplementedError("TODO")

    def transact(self, *args, **kwargs):
        raise NotImplementedError("TODO")


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


def parse_contract_abi(contract_abi):
    """
    Parse a contract ABI into Function and Event objects.
    """
    constructor = None
    _functions = collections.defaultdict(list)
    events = {}

    # Loop over all of the items in the contract ABI and construct Function or
    # Event objects for them.
    for signature_item in contract_abi:
        if signature_item['type'] == 'constructor':
            # Constructors don't need to be part of a contract's methods
            if signature_item.get('inputs'):
                constructor = Function(
                    name='constructor',
                    inputs=signature_item['inputs'],
                )
            continue

        if signature_item['type'] == 'function':
            # make sure we're not overwriting a signature

            func = Function(
                name=signature_item['name'],
                inputs=signature_item['inputs'],
                outputs=signature_item['outputs'],
                constant=signature_item['constant'],
            )
            _functions[signature_item['name']].append(func)

        elif signature_item['type'] == 'event':
            if signature_item['name'] in events:
                # TODO: handle namespace conflicts
                raise ValueError("Duplicate Event name: {0}".format(signature_item['name']))  # NOQA
            event = Event(
                name=signature_item['name'],
                inputs=signature_item['inputs'],
                anonymous=signature_item['anonymous'],
            )
            events[event.name] = event
        else:
            raise ValueError("Unknown signature item '{0}'".format(signature_item))

    # Find sets of functions that have the same name and wrap them in
    # FunctionGroup objects.
    functions = []

    for fn_list in _functions.values():
        if len(fn_list) == 1:
            functions.append(fn_list[0])
        else:
            fn_group = FunctionGroup(fn_list)
            functions.append(fn_group)

    return constructor, events, functions


def construct_contract_class(contract_abi,
                             contract_name=None,
                             contract_code=None,
                             contract_runtime=None,
                             contract_source=None):
    constructor, events, functions = parse_contract_abi(contract_abi)

    if contract_name is None and constructor is not None:
        contract_name = constructor.name
    elif contract_name is None and contract_source is not None:
        try:
            contract_name = get_contract_name_from_source(contract_source)
        except ValueError:
            pass

    docstring = construct_contract_docstring(
        contract_name=contract_name,
        constructor_sig=str(constructor) if constructor else "",
        function_sigs=[str(fn) for fn in functions],
        event_sigs=[str(fn) for fn in events],
    )

    _dict = {
        '__doc__': docstring,
        'name': contract_name,
        'constructor': constructor,
        'events': events,
        'functions': functions,
        'code': contract_code,
        'runtime': contract_runtime,
        'source': contract_source,
    }

    return type(str(contract_name), (ContractBase,), _dict)
