#!/usr/bin/env python3
"""
A minimal, safe deserialization helper that accepts only a whitelist of
trusted formats.  The implementation intentionally limits the supported
formats to avoid accidental execution of unsafe code (e.g., `pickle`).

The function accepts raw bytes and a format name, returning the decoded
Python object when the format is allowed.  Unsupported or dangerous formats
raise a `ValueError`.

This module follows the principle of least privilege and protects against
CWE-664 (Improper Control of a Resource Through its Lifetime) by ensuring
that the deserialization logic is tightly controlled and not exposed to
untrusted input beyond the allowed formats.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from typing import Any


# Whitelist of safe formats.
ALLOWED_FORMATS = {
    "json": json.loads,
    # XML parsing is considered safe for simple data structures
    # but still has potential security issues if used with complex XML.
    "xml": ET.fromstring,
}


def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `data_bytes` according to the specified `format_name`.

    Parameters
    ----------
    data_bytes : bytes
        Serialized object in byte format.
    format_name : str
        Name of the serialization format. Supported values are
        ``"json"`` and ``"xml"``.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not in the whitelist of allowed formats.
    """
    if format_name not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format: {format_name!r}. "
            f"Allowed formats are: {', '.join(ALLOWED_FORMATS)}."
        )

    # Decode bytes to string for text-based formats.
    if format_name == "json":
        try:
            # Ensure UTF-8 decoding; errors='strict' will raise on invalid data.
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON format") from exc

        try:
            return ALLOWED_FORMATS[format_name](text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if format_name == "xml":
        try:
            # ElementTree expects a string or bytes; we pass the raw bytes.
            return ALLOWED_FORMATS[format_name](data_bytes)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # The code should never reach here because of the whitelist check.
    raise ValueError(f"Unhandled format: {format_name!r}")