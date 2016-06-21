def test_abi_signatures(LogsEvents):
    assert LogsEvents.SingleIndex.abi_signature == 3842580050
    assert LogsEvents.SingleIndex.encoded_abi_signature == b'\xe5\t\x1eR'
    assert LogsEvents.SingleIndex.event_topic == b'0xe5091e521791fb0fb6be999dcb6d5031d9f0a8032185b13790f8d2f95e163b1f'

    assert LogsEvents.DoubleIndex.abi_signature == 2525890609
    assert LogsEvents.DoubleIndex.encoded_abi_signature == b'\x96\x8e\x081'
    assert LogsEvents.DoubleIndex.event_topic == b'0x968e08311bcc13cd5d4feae6a3c87bedb195ab51905c8ec75a10580b5b5854c7'
