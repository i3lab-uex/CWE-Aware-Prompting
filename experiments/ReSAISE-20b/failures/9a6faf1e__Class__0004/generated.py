#!/usr/bin/env python3
"""
Secure deserialization helper.

The function `read_serialized_file` only accepts a strict whitelist of
serialization formats.  Any format that can execute arbitrary code (e.g.
`pickle`) is rejected with a ValueError.  This mitigates CWE‑913
“Improper Control of Dynamically‑Managed Code Resources”.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union


# --------------------------------------------------------------------------- #
# Whitelist of safe formats
# --------------------------------------------------------------------------- #
_SAFE_FORMATS = {
    "json": _deserialize_json,
    "text": _deserialize_text,
}


# --------------------------------------------------------------------------- #
# Deserialization helpers
# --------------------------------------------------------------------------- #
def _deserialize_json(file_obj) -> Any:
    """Deserialize JSON data from a file object."""
    return json.load(file_obj)


def _deserialize_text(file_obj) -> str:
    """Return the raw text from a file object."""
    return file_obj.read()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def read_serialized_file(file_path: str | Path, file_format: str) -> Any:
    """
    Safely read and deserialize data from *file_path*.

    Parameters
    ----------
    file_path : str | Path
        The path to the serialized data file.
    file_format : str
        The format of the serialization. Must be one of the whitelisted
        values (currently: "json", "text").

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *file_format* is not in the whitelist or if an unsafe format
        (e.g. "pickle") is requested.
    FileNotFoundError
        If the file does not exist or cannot be opened.

    Notes
    -----
    The function opens files in binary mode for JSON to support UTF‑8
    decoding and text mode for plain text.  No arbitrary code execution
    occurs during deserialization.
    """
    # Normalise format name
    fmt = file_format.lower()

    if fmt not in _SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: '{file_format}'. "
            f"Allowed formats are: {', '.join(_SAFE_FORMATS)}"
        )

    # Determine mode based on format
    open_mode = "rb" if fmt == "json" else "r"

    path = Path(file_path)
    with path.open(open_mode, encoding="utf-8" if fmt != "text" else None) as f:
        return _SAFE_FORMATS[fmt](f)


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     data = read_serialized_file("data.json", "json")
#     print(data)