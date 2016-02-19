

def test_double_index_event(deployed_logs_events, blockchain_client):
    """
    This is a really week test but I'm not sure what to test yet.
    """
    txn_a_hash = deployed_logs_events.logDoubleIndex('test-key-a', 'test-key-b', 'test-val_a', 12345)
    txn_b_hash = deployed_logs_events.logSingleIndex('test-key-a', 'test-val_a', 12345)

    txn_receipt = blockchain_client.get_transaction_receipt(txn_a_hash)

    logs_from_a = deployed_logs_events.DoubleIndex.get_transaction_logs(txn_a_hash)
    logs_from_b = deployed_logs_events.DoubleIndex.get_transaction_logs(txn_b_hash)
    assert len(logs_from_a) == 1
    assert len(logs_from_b) == 0
