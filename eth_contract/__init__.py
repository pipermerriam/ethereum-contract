import pkg_resources

from eth_contract.core import (  # NOQA
    construct_contract_class,
)


__version__ = pkg_resources.get_distribution('ethereum-contract').version
