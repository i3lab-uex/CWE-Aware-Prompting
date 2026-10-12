#!/usr/bin/env python3
"""
Secure deserialization of byte streams.

This module defines a single function, :func:`decode_data_stream`, which
converts a byte stream into its corresponding Python object.  Only a small
set of explicitly safe formats is supported; any other format raises a
:class:`ValueError`.  The implementation deliberately avoids executing
arbitrary code or importing modules based on user input, thereby mitigating
CWE‑913 and related security concerns.
"""

from __future__ import annotations

import json
import struct
import zlib
from typing import Any

# --------------------------------------------------------------------------- #
# Supported formats (add more only after careful security review)
# --------------------------------------------------------------------------- #
_SUPPORTED_FORMATS = {
    "json": _decode_json,
    "zlib-json": _decode_zlib_json,  # compressed JSON
}

def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    data : bytes
        The serialized data stream.
    data_format : str
        One of the supported format identifiers:
        * ``"json"``
        * ``"zlib-json"`` – a zlib‑compressed JSON payload.

    Returns
    -------
    Any
        The Python object represented by the input stream.

    Raises
    ------
    ValueError
        If *data_format* is not among the supported formats.
    """
    decoder = _SUPPORTED_FORMATS.get(data_format.lower())
    if decoder is None:
        raise ValueError(
            f"Unsupported or unsafe data format '{data_format}'. "
            "Allowed formats: " + ", ".join(_SUPPORTED_FORMATS.keys())
        )
    return decoder(data)


# --------------------------------------------------------------------------- #
# Decoder implementations
# --------------------------------------------------------------------------- #

def _decode_json(data: bytes) -> Any:
    """
    Decode a JSON payload.

    The data must be UTF‑8 encoded.  ``json.loads`` is safe for arbitrary
    input because it does not execute code.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF-8") from exc
    return json.loads(text)


def _decode_zlib_json(data: bytes) -> Any:
    """
    Decode a zlib‑compressed JSON payload.

    The compressed data is first decompressed using ``zlib.decompress``.
    Errors in decompression or JSON parsing are wrapped into
    :class:`ValueError` to keep the public API simple.
    """
    try:
        decompressed = zlib.decompress(data)
    except zlib.error as exc:
        raise ValueError("Failed to decompress data with zlib") from exc
    return _decode_json(decompressed)


# --------------------------------------------------------------------------- #
# End of module
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Basic self‑test when executed directly
    import sys

    test_json = json.dumps({"foo": "bar", "numbers": [1, 2, 3]}).encode("utf-8")
    compressed = zlib.compress(test_json)

    for fmt, payload in [("json", test_json), ("zlib-json", compressed)]:
        obj = decode_data_stream(payload, fmt)
        print(f"Decoded {fmt!r} ->", obj)

    # Test unsupported format
    try:
        decode_data_stream(b"{}", "pickle")
    except ValueError as e:
        print("Caught expected exception:", e, file=sys.stderr)