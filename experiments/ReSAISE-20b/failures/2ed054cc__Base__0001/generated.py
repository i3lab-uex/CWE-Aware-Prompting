#!/usr/bin/env python3
"""
Secure deserialization of untrusted raw data.

Only JSON and XML formats are supported.  The implementation uses
the `defusedxml` library to protect against XML External Entity (XXE)
attacks and other XML-based vulnerabilities.
"""

from __future__ import annotations

import json
from typing import Any

# `defusedxml` is a lightweight wrapper around the standard library
# that sanitises XML input to mitigate XXE and other attacks.
try:
    from defusedxml import ElementTree as ET
except ImportError as exc:  # pragma: no cover
    raise RuntimeError(
        "defusedxml is required for secure XML deserialization. "
        "Install it with: pip install defusedxml"
    ) from exc


# Allowed serialization formats
ALLOWED_FORMATS = {"json", "xml"}


def _decode_bytes(raw_data: bytes) -> str:
    """
    Decode raw data to a UTF-8 string.  If decoding fails, raise ValueError.
    """
    try:
        return raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise ValueError("Data is not valid UTF-8") from exc


def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely convert serialized data to a Python object.

    Parameters
    ----------
    raw_data : bytes
        Serialized representation of the data.
    serialization_format : str
        The format used for serialization.  Supported values are
        "json" and "xml".

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported, the data cannot be decoded,
        or deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported serialization format: {serialization_format!r}")

    # JSON deserialization
    if fmt == "json":
        text = _decode_bytes(raw_data)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError("Invalid JSON data") from exc

    # XML deserialization (safe)
    if fmt == "xml":
        text = _decode_bytes(raw_data)
        try:
            # defusedxml.ElementTree.fromstring is safe against XXE
            return ET.fromstring(text)
        except ET.ParseError as exc:  # pragma: no cover
            raise ValueError("Invalid XML data") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {serialization_format!r}")