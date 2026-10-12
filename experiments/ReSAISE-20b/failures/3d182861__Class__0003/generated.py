#!/usr/bin/env python3
"""
Secure deserialization helper.

This module exposes a single function `deserialize_content` that can safely
convert byte streams into Python objects for a limited set of formats.
Only JSON and plain HTML are supported. Any other format is rejected to
prevent potential code injection or arbitrary object creation.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import json
import html
from typing import Any


def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using a restricted set of formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream to deserialize.
    data_format : str
        One of the supported formats: 'json' or 'html'.

    Returns
    -------
    Any
        The deserialized Python object. For 'json' this will be a dict/list/etc.
        For 'html', the returned value is a string with HTML entities decoded.

    Raises
    ------
    ValueError
        If `data_format` is not supported or considered insecure.
    """
    # Normalise the format string
    fmt = data_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to str using UTF-8 (common default for JSON)
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 encoding for JSON data: {exc}") from exc

        # json.loads is safe for arbitrary JSON; it does not execute code.
        return json.loads(text)

    if fmt == "html":
        # For HTML we simply decode and unescape entities.
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 encoding for HTML data: {exc}") from exc

        return html.unescape(text)

    # Unsupported or insecure formats
    raise ValueError(f"Unsupported or insecure deserialization format: '{data_format}'")