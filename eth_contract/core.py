import collections

from rlp.utils import (
    encode_hex,
)

from eth_contract.functions import (
    Function,
    FunctionGroup,
)
from eth_contract.utils import (
    get_contract_name_from_source,
    construct_contract_docstring,
)
from eth_contract.events import Event
from eth_contract.utils import (
    str_to_bytes,
)


class ContractBase(object):
    name = None
    constructor = None
    events = None
    functions = None
    code = None
    runtime = None
    source = None

    def __str__(self):
        return str(self.name if self.name else "Unknown")

    @classmethod
    def new(address):
        raise NotImplementedError("TODO")

    @classmethod
    def at(address):
        raise NotImplementedError("TODO")


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

    for fn_name, fn_list in _functions.items():
        if len(fn_list) == 1:
            functions.append(fn_list[0])
        else:
            fn_group = FunctionGroup(fn_list)
            functions.append(fn_group)

    return constructor, events, functions


def contract(contract_abi, contract_name=None, contract_code=None,
             contract_runtime=None, contract_source=None):
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
