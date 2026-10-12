#!/usr/bin/env python3
"""
Secure deserialization of byte streams.

Supported formats (safe):
    - json   : JSON format
    - yaml   : YAML using safe_load
    - msgpack: MessagePack (if available)

Unsupported formats (e.g. pickle, html) raise ValueError.

CWE-502: Deserialization of Untrusted Data
"""

from __future__ import annotations

import json
from typing import Any, Dict

try:
    # Optional dependency; only used if available.
    import msgpack
except ImportError:  # pragma: no cover
    msgpack = None

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


# Mapping of allowed formats to their deserialization functions.
_ALLOWED_FORMATS: Dict[str, Any] = {
    "json": lambda data: json.loads(data.decode("utf-8")),
}

# Add YAML if available
if yaml is not None:  # pragma: no cover
    _ALLOWED_FORMATS["yaml"] = lambda data: yaml.safe_load(data.decode("utf-8"))

# Add MessagePack if available
if msgpack is not None:  # pragma: no cover
    _ALLOWED_FORMATS["msgpack"] = lambda data: msgpack.unpackb(data, raw=False)


def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The format of the serialized data. Must be one of the supported types.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = serialization_type.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization type: {serialization_type!r}. "
            f"Allowed types are: {', '.join(sorted(_ALLOWED_FORMATS))}"
        )

    try:
        obj = _ALLOWED_FORMATS[fmt](byte_data)
    except Exception as exc:  # pragma: no cover
        raise ValueError(
            f"Failed to deserialize data as {serialization_type!r}: {exc}"
        ) from exc

    return obj