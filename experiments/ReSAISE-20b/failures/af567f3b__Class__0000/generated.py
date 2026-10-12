#!/usr/bin/env python3
"""
Secure deserialization helper.

Only the 'json' format is supported to avoid unsafe data handling.
Any other format raises a ValueError.
"""

import json
from typing import Any


def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize the given byte stream into a Python object.

    Parameters
    ----------
    input_data : bytes
        The serialized data that needs to be deserialized.
    input_format : str
        A string indicating the deserialization format. Only 'json' is allowed.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    # Normalize and validate format string
    fmt = input_format.strip().lower()
    if fmt != "json":
        raise ValueError(
            f"Unsupported or insecure deserialization format: '{input_format}'. "
            "Only 'json' is allowed."
        )

    # Decode bytes to string safely
    try:
        decoded_str = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8 encoded JSON.") from exc

    # Parse JSON safely
    try:
        return json.loads(decoded_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Input data is not valid JSON.") from exc