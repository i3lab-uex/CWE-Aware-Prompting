#!/usr/bin/env python3
"""
Secure deserialization helper.

This module provides a single function, `security_content_deserializer`, which
deserializes data from an external source into a Python object.  Only formats
explicitly considered safe are allowed; all other formats raise `ValueError`.
The implementation guards against the common pitfalls of deserializing
untrusted data, especially avoiding the use of `pickle` or other unsafe
mechanisms.

Supported formats:
- ``json``: JSON data encoded as UTF‑8 bytes.
"""

from __future__ import annotations

import json
from typing import Any


def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using a *safe* format.

    Parameters
    ----------
    byte_stream : bytes
        The raw serialized data.  For JSON, the data must be UTF‑8 encoded.
    data_format : str
        The name of the serialization format.  Only ``'json'`` is accepted.
        Any other value results in a :class:`ValueError`.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If ``data_format`` is not one of the supported safe formats.
    json.JSONDecodeError
        If the byte stream does not contain valid JSON data.

    Notes
    -----
    The function deliberately rejects potentially unsafe formats such as
    ``pickle``, ``marshal`` or any binary protocols that can execute code on
    deserialization.  The implementation is intentionally minimal to avoid
    introducing new attack vectors.
    """
    # Normalise the format string to lower case for comparison
    fmt = data_format.strip().lower()

    if fmt != "json":
        raise ValueError(
            f"Unsupported or insecure data format '{data_format}'. "
            "Only 'json' is permitted."
        )

    # JSON data must be UTF‑8 encoded.  Decode first, then parse.
    try:
        text = byte_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "Byte stream is not valid UTF‑8 encoded JSON data."
        ) from exc

    # The json module is safe for deserializing untrusted input when used
    # with the default parameters.  No custom hooks are provided to avoid
    # executing arbitrary code.
    return json.loads(text)