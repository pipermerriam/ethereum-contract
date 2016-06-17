def test_contract_return13_function_signature(deployed_math):
    assert deployed_math.return13.abi_signature == 371289913
    assert deployed_math.return13.encoded_abi_signature == b'\x16!o9'
    assert deployed_math.return13.get_call_data([]) == b'16216f39'


def test_contract_add_function_signature(deployed_math):
    assert deployed_math.add.abi_signature == 2784215611
    assert deployed_math.add.encoded_abi_signature == b'\xa5\xf3\xc2;'
    assert deployed_math.add.get_call_data((3, 4)) == b'a5f3c23b00000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000004'


def test_contract_multiply7_function_signature(deployed_math):
    assert deployed_math.multiply7.abi_signature == 3707058097
    assert deployed_math.multiply7.encoded_abi_signature == b'\xdc\xf57\xb1'
    assert deployed_math.multiply7.get_call_data((3,)) == b'dcf537b10000000000000000000000000000000000000000000000000000000000000003'


def test_contract_function_call_return13(deployed_math):
    ret = deployed_math.return13.call()
    assert ret == 13


def test_contract_function_call_multiply7(deployed_math):
    ret = deployed_math.multiply7.call(3)
    assert ret == 21


def test_contract_function_call_add(deployed_math):
    ret = deployed_math.add.call(25, 35)
    assert ret == 60


def test_sent_transaction_with_value(deployed_math, blockchain_client):
    assert deployed_math.get_balance() == 0
    deployed_math.add.sendTransaction(35, 45, value=1000)
    assert deployed_math.get_balance() == 1000


def test_syncronous_transaction_sending(deployed_math, blockchain_client):
    assert deployed_math.get_balance() == 0
    txn_h, txn_r = deployed_math.add.s(35, 45, value=1000)
    assert deployed_math.get_balance() == 1000
