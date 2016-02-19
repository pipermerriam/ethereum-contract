import pkg_resources

from eth_contract.functions import (  # NOQA
    Function,
    FunctionGroup,
)
from eth_contract.events import Event  # NOQA
from eth_contract.core import (  # NOQA
    Contract,
)


__version__ = pkg_resources.get_distribution('ethereum-contract').version
