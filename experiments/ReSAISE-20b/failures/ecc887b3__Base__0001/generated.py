#!/usr/bin/env python3
"""
safe_deserialize.py

Safely deserialize a byte string into a Python object for a limited set of
trusted formats.  Untrusted data is only accepted if the format has been
explicitly whitelisted.

Supported formats:
    - json  : JSON, parsed with the standard library
    - xml   : XML, parsed with defusedxml to mitigate XXE attacks

Any other format will raise a ValueError.
"""

import json
from typing import Any

# defusedxml provides an XML parser that protects against XXE and other
# XML-based attacks.  It is a drop‑in replacement for xml.etree.ElementTree.
try:
    from defusedxml import ElementTree as ET
except ImportError:  # pragma: no cover
    raise RuntimeError(
        "defusedxml is required for safe XML deserialization. "
        "Install it with `pip install defusedxml`."
    )

# Whitelist of allowed formats
_ALLOWED_FORMATS = {"json", "xml"}


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Deserialize a byte string into a Python object only if the format is
    explicitly allowed.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte string containing the serialized data.
    allowed_format : str
        One of the supported format names: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    fmt = allowed_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    try:
        if fmt == "json":
            # JSON is text; decode bytes using UTF‑8
            return json.loads(serialized_bytes.decode("utf-8"))
        elif fmt == "xml":
            # XML is parsed with defusedxml to avoid XXE attacks
            return ET.fromstring(serialized_bytes)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize data as {allowed_format!r}: {exc}") from exc