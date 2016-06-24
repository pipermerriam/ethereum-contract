import pkg_resources

from eth_contract.core import (  # NOQA
    contract,
)


__version__ = pkg_resources.get_distribution('ethereum-contract').version
