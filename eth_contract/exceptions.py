class EncodingError(Exception):
    pass


class ValueOutOfBounds(EncodingError):
    """
    Raised when trying to encode a value which is out bounds for the desired
    type.
    """
    pass


class DecodingError(Exception):
    pass


class EmptyDataError(DecodingError):
    """
    Raised when a call to a function unexpectedly returns empty data `0x` when
    a response was expected.
    """
    pass
