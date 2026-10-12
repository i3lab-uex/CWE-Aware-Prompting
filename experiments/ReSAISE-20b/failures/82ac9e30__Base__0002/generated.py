#!/usr/bin/env python3
"""
Secure deserialization helper.

The module exposes a single function :func:`deserialize_data` that accepts
a byte stream and the name of the serialization method used to create it.
Only a small, vetted set of deserialization routines is allowed.  Any
attempt to use an unsupported or potentially unsafe format results in a
``ValueError``.

This design protects against the CWE‑502 vulnerability (Deserialization of Untrusted Data)
by explicitly whitelisting safe deserializers and avoiding the use of
Python's ``pickle`` or other generic binary formats that can execute code.
"""

import json
import csv
import io
from typing import Any, Callable

# Whitelisted deserialization methods and their corresponding handlers.
SAFE_DESERIALIZERS: dict[str, Callable[[bytes], Any]] = {}


def _json_deserializer(data: bytes) -> Any:
    """Deserialize JSON data from a UTF‑8 encoded byte stream."""
    text = data.decode("utf-8")
    return json.loads(text)


def _csv_deserializer(data: bytes) -> list[dict[str, str]]:
    """
    Deserialize CSV data from a UTF‑8 encoded byte stream.
    Returns a list of dictionaries (one per row), using the first
    line as column headers.
    """
    text = data.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    return [row for row in reader]


# Register safe deserializers
SAFE_DESERIALIZERS["json"] = _json_deserializer
SAFE_DESERIALIZERS["csv"] = _csv_deserializer


def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_stream : bytes
        The raw serialized data.
    deserialization_method : str
        Identifier of the serialization format (e.g. 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided method is not in the whitelist or cannot be deserialized.
    """
    if deserialization_method not in SAFE_DESERIALIZERS:
        raise ValueError(
            f"Deserialization method '{deserialization_method}' is not allowed."
        )

    deserializer = SAFE_DESERIALIZERS[deserialization_method]
    try:
        return deserializer(data_stream)
    except Exception as exc:  # pragma: no cover
        # Wrap any exception from the deserializer to provide a clear error message.
        raise ValueError(
            f"Failed to deserialize data using method '{deserialization_method}'."
        ) from exc