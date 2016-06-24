from rlp.utils import (
    int_to_big_endian,
    big_endian_to_int,
)

from eth_abi import decode_abi
from eth_abi.utils import (
    zpad,
)
from eth_contract.utils import (
    sha3,
    str_to_bytes,
)


class ContractBound(object):
    _contract = None

    def _bind(self, contract):
        self._contract = contract

    @property
    def contract(self):
        if self._contract is None:
            raise AttributeError("Function not bound to a contract")
        return self._contract

    #
    # ABI Signature
    #
    @property
    def input_types(self):
        """
        Iterable of the types this function takes.
        """
        if self.inputs:
            return [i['type'] for i in self.inputs]
        return []

    @property
    def signature(self):
        signature = "{name}({arg_types})".format(
            name=self.name,
            arg_types=','.join(self.input_types),
        )
        return str_to_bytes(signature)

    @property
    def abi_signature(self):
        """
        Compute the bytes4 signature for the object.
        """
        return big_endian_to_int(sha3(str_to_bytes(self.signature))[:4])

    @property
    def encoded_abi_signature(self):
        return zpad(int_to_big_endian(self.abi_signature), 4)

    @property
    def output_types(self):
        """
        Iterable of the types this function takes.
        """
        if self.outputs:
            return [i['type'] for i in self.outputs]
        return []

    def cast_return_data(self, outputs, raw=False):
        values = decode_abi(self.output_types, outputs)

        if not raw and len(self.output_types) == 1:
            return values[0]

        return values
