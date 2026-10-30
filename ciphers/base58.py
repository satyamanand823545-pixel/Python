"""
Base58 encoding and decoding using the Bitcoin alphabet.

https://en.wikipedia.org/wiki/Base58
"""

BASE58_CHARSET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58_encode(data: bytes) -> str:
    """Encode bytes using the Bitcoin Base58 alphabet.

    Leading zero bytes are represented by leading ``1`` characters.

    >>> base58_encode(b"")
    ''
    >>> base58_encode(b"\\x00\\x01")
    '12'
    >>> base58_encode(b"Hello World!")
    '2NEpo7TZRRrLZSi2U'
    >>> base58_encode(b"\\x00\\x00")
    '11'
    """
    if not isinstance(data, bytes):
        msg = f"a bytes-like object is required, not '{data.__class__.__name__}'"
        raise TypeError(msg)

    leading_zeroes = len(data) - len(data.lstrip(b"\x00"))
    value = int.from_bytes(data, byteorder="big")
    encoded_digits = []
    while value:
        value, remainder = divmod(value, len(BASE58_CHARSET))
        encoded_digits.append(BASE58_CHARSET[remainder])

    return "1" * leading_zeroes + "".join(reversed(encoded_digits))


def base58_decode(encoded_data: str) -> bytes:
    """Decode a Bitcoin Base58 string to bytes.

    Leading ``1`` characters are decoded as leading zero bytes.

    >>> base58_decode("")
    b''
    >>> base58_decode("12")
    b"\\x00\\x01"
    >>> base58_decode("2z")
    b's'
    >>> base58_decode("2NEpo7TZRRrLZSi2U")
    b'Hello World!'
    >>> base58_decode("11")
    b"\\x00\\x00"
    >>> base58_decode("0")
    Traceback (most recent call last):
      ...
    ValueError: Invalid Base58 character: '0'
    """
    if not isinstance(encoded_data, str):
        msg = f"encoded_data must be a string, not '{encoded_data.__class__.__name__}'"
        raise TypeError(msg)

    value = 0
    for character in encoded_data:
        try:
            digit = BASE58_CHARSET.index(character)
        except ValueError:
            raise ValueError(f"Invalid Base58 character: {character!r}") from None
        value = value * len(BASE58_CHARSET) + digit

    leading_zeroes = len(encoded_data) - len(encoded_data.lstrip("1"))
    decoded = (
        value.to_bytes((value.bit_length() + 7) // 8, byteorder="big") if value else b""
    )
    return b"\x00" * leading_zeroes + decoded


if __name__ == "__main__":
    import doctest

    doctest.testmod()
