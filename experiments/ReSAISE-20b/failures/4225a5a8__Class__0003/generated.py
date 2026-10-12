#!/usr/bin/env python3
"""
Secure deserialization helper.

This module provides a single function, :func:`objectify_data`, that
converts a byte‑encoded representation of data into a native Python object.
Only a limited set of formats are allowed (JSON and XML).  Any other format
is considered unsafe and will raise a :class:`ValueError`.

The implementation uses the `defusedxml` package to protect against
XML bombs and other XML related attacks.  No `pickle`, `yaml` or other
potentially unsafe deserializers are supported.
"""

from __future__ import annotations

import json
from typing import Any, Union

# `defusedxml` is a small dependency that mitigates XML attacks.
# If it is not installed, the user will receive an ImportError with a clear
# message.  It is intentionally required for XML support.
try:
    from defusedxml.ElementTree import fromstring as xml_fromstring
except ImportError as exc:
    raise ImportError(
        "defusedxml is required for XML deserialization. "
        "Install it via `pip install defusedxml`."
    ) from exc


def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize *raw_data* according to the specified *method_name*.

    Parameters
    ----------
    raw_data : bytes
        Serialized data in byte form.
    method_name : str
        One of ``'json'`` or ``'xml'``.  Any other value will raise
        :class:`ValueError`.

    Returns
    -------
    object
        The deserialized Python representation.  For JSON this will be a
        ``dict`` or ``list``; for XML an :class:`xml.etree.ElementTree.Element`.

    Raises
    ------
    TypeError
        If *raw_data* is not of type :class:`bytes`.
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    if not isinstance(raw_data, bytes):
        raise TypeError(f"raw_data must be bytes; got {type(raw_data).__name__}")

    method = method_name.lower()

    if method == "json":
        try:
            # json.loads accepts str, so decode using utf-8 (common encoding).
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "xml":
        try:
            # defusedxml protects against XML bombs and other attacks.
            return xml_fromstring(raw_data)
        except Exception as exc:  # Catch broad because defusedxml may raise various types
            raise ValueError("Invalid or unsafe XML data") from exc

    # Any other method is considered dangerous.
    raise ValueError(f"Unsupported deserialization format: {method_name}")