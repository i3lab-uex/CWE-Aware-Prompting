#!/usr/bin/env python3
"""
Secure deserialization of untrusted byte streams.

Supported formats (safe, predefined):
  - json
  - yaml

Unsupported or insecure formats raise ValueError.
"""

import json
from typing import Any

# Optional dependency – only imported if needed and available.
try:
    import yaml  # PyYAML
except ImportError:   # pragma: no cover – not required for all environments
    yaml = None


def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize `input_data` according to `input_format`.

    Parameters
    ----------
    input_data : bytes
        The serialized data.
    input_format : str
        Format identifier (case‑insensitive). Supported values are
        'json' and 'yaml'.

    Returns
    -------
    Any
        The Python object represented by the input data.

    Raises
    ------
    ValueError
        If `input_format` is unsupported or insecure.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = input_format.lower()

    # Decode bytes to string using UTF‑8; errors are replaced to avoid
    # crashes from malformed data, but the decoded string is still
    # processed by the safe loaders.
    try:
        text = input_data.decode("utf-8", errors="replace")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to decode input data") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        if yaml is None:  # pragma: no cover
            raise ValueError("YAML support not available (missing PyYAML)")
        try:
            # safe_load restricts the tags that can be parsed.
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:  # pragma: no cover
            raise ValueError("Invalid YAML data") from exc

    # Any other format is considered insecure or unsupported.
    raise ValueError(f"Unsupported deserialization format: {input_format}")