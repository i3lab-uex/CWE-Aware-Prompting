#!/usr/bin/env python3
"""
Secure deserialization helper.

Only a small, explicitly whitelisted set of formats is allowed.  The
function accepts a bytes stream and a format string, and returns the
Python object reconstructed from that stream.  Unsupported or unsafe
formats raise a ValueError.

CWE-502 (Deserialization of Untrusted Data) is mitigated by
strictly limiting the formats that can be processed and by avoiding
dangerous modules such as `pickle` or `yaml.Loader`.
"""

from __future__ import annotations

import json
import msgpack  # type: ignore[import]   # optional, only used if enabled
from typing import Any


# Whitelist of safe formats.  Extend this list only after careful security
# review.
ALLOWED_FORMATS = {
    "json",
    # "msgpack",  # uncomment if msgpack is considered safe in your context
}


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    serialization_format : str
        One of the allowed format names (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    try:
        if fmt == "json":
            # JSON requires a text string; decode using UTF-8.
            return json.loads(stream.decode("utf-8"))
        # Uncomment the following block if msgpack is added to ALLOWED_FORMATS.
        #
        # elif fmt == "msgpack":
        #     return msgpack.unpackb(stream, raw=False)
    except Exception as exc:
        # Wrap any parsing exception to avoid leaking implementation details.
        raise ValueError(f"Failed to deserialize {serialization_format!r} data") from exc

    # If we reach here, the format was somehow accepted but not handled.
    raise ValueError(f"Deserializer for {serialization_format!r} is unimplemented")