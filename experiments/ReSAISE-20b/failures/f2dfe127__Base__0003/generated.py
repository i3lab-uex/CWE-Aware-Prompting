#!/usr/bin/env python3
"""
Safe deserialization of bytes into Python objects.

Supported formats: 'json', 'xml'.

The function deliberately avoids unsafe formats such as pickle or
yaml, which can execute arbitrary code during deserialization.
"""

import json
import xml.etree.ElementTree as ET
from typing import Any


def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize a byte string into a Python object using a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data to be deserialized.
    format_name : str
        Name of the serialization format. Supported values are:
            - 'json'
            - 'xml'

    Returns
    -------
    Any
        The deserialized Python object. For JSON this can be a dict,
        list, str, int, float, bool or None. For XML it returns an
        :class:`xml.etree.ElementTree.Element` tree.

    Raises
    ------
    ValueError
        If `format_name` is not among the supported formats.
    TypeError
        If `data_bytes` is not of type bytes.
    """
    if not isinstance(data_bytes, bytes):
        raise TypeError("data_bytes must be of type 'bytes'")

    fmt = format_name.lower()
    if fmt == "json":
        # Decode bytes to string using UTF-8, then load JSON.
        text = data_bytes.decode("utf-8")
        return json.loads(text)

    if fmt == "xml":
        # Parse XML bytes directly; ElementTree.fromstring accepts bytes.
        return ET.fromstring(data_bytes)

    # Unsupported format
    raise ValueError(
        f"Unsupported serialization format: {format_name!r}. "
        "Only 'json' and 'xml' are permitted."
    )