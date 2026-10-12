#!/usr/bin/env python3
"""
Secure deserialization helper.

This module defines `restore_object_from_stream`, which accepts a bytes object
and a format string, and reconstructs the corresponding Python object only for
whitelisted, safe serialization formats. Unsupported or potentially unsafe
formats raise a ValueError.

Supported formats:
    * json   – standard JSON (text based, safe)
    * msgpack – MessagePack binary format (requires the external `msgpack`
                library; considered safe when used with default options)

The function intentionally avoids `pickle`, `yaml` (unsafe by default), and
any other format that could execute arbitrary code during deserialization.
"""

from __future__ import annotations

import json
from typing import Any, Callable

# Optional: try to import msgpack; if unavailable we simply skip it
try:
    import msgpack  # type: ignore
except ImportError:  # pragma: no cover
    msgpack = None

# Mapping of allowed format names to their corresponding deserialization callables.
# Each callable takes a bytes object and returns the reconstructed Python object.
_ALLOWED_FORMATS: dict[str, Callable[[bytes], Any]] = {}

# JSON deserialization – safe by default
def _deserialize_json(data: bytes) -> Any:
    """
    Decode JSON data from UTF‑8 encoded bytes.
    Raises json.JSONDecodeError if the input is invalid.
    """
    return json.loads(data.decode("utf-8"))

_ALLOWED_FORMATS["json"] = _deserialize_json

# MessagePack deserialization – safe if `msgpack` is available
if msgpack:
    def _deserialize_msgpack(data: bytes) -> Any:
        """
        Decode MessagePack data.
        The default `raw=True` option preserves bytes for string values,
        which is the safest behaviour.
        """
        return msgpack.unpackb(data, raw=True)

    _ALLOWED_FORMATS["msgpack"] = _deserialize_msgpack


def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Reconstruct a Python object from the given byte stream using a safe,
    whitelisted serialization format.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The name of the serialization format (e.g., 'json', 'msgpack').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not in the whitelist of safe formats.
    """
    # Normalise the format name to lower case for case‑insensitive matching
    fmt = serialization_type.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: '{serialization_type}'. "
            "Allowed formats are: " + ", ".join(_ALLOWED_FORMATS.keys())
        )

    # Retrieve the corresponding deserializer
    deserializer = _ALLOWED_FORMATS[fmt]

    try:
        return deserializer(byte_data)
    except Exception as exc:  # pragma: no cover
        # Wrap any exception to provide a consistent error type
        raise ValueError(
            f"Failed to deserialize data as '{serialization_type}': {exc}"
        ) from exc