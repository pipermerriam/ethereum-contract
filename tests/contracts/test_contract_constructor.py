import json

from eth_contract import construct_contract_class


def test_abi_only_contract_class_construction(CONTRACT_ABI):
    Math = construct_contract_class(CONTRACT_ABI, contract_name="Math")

    assert str(Math) == "<class 'eth_contract.core.Math'>"
    assert Math.code == None
    assert Math.runtime == None
    assert Math.source == None

    assert len(Math.functions) == 5
    assert len(Math.events) == 1


def test_full_contract_class_construction(CONTRACT_ABI, CONTRACT_CODE,
                                          CONTRACT_RUNTIME, CONTRACT_SOURCE):
    Math = construct_contract_class(CONTRACT_ABI,
                                    contract_name="Math",
                                    contract_code=CONTRACT_CODE,
                                    contract_runtime=CONTRACT_RUNTIME,
                                    contract_source=CONTRACT_SOURCE)

    assert str(Math) == "<class 'eth_contract.core.Math'>"
    assert Math.code == CONTRACT_CODE
    assert Math.runtime == CONTRACT_RUNTIME
    assert Math.source == CONTRACT_SOURCE

    assert len(Math.functions) == 5
    assert len(Math.events) == 1
