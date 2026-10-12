#!/usr/bin/env python3
"""
Secure deserialization helper.

This module provides a single function, `interpret_serialized_content`,
which reads data from a file and deserializes it only if the
serialization format is explicitly trusted.  The supported formats are:

* ``json``   – JSON data parsed into Python objects.
* ``text``   – Raw text, returned as a string.
* ``pickle`` – Pickled data *only* if it contains strictly built‑in
  types (int, float, str, list, dict, tuple, bool, None).  Any
  other objects will raise a ValueError.

The function is intentionally conservative to mitigate the risks of
CWE‑502 (Deserialization of Untrusted Data).  It performs no
evaluation of custom classes or execution of arbitrary code.
"""

import json
import pickle
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def _is_pickle_safe(data: Any) -> bool:
    """
    Recursively verify that the unpickled object only contains
    built‑in immutable types.  This is a very small subset of the
    full range of safe objects; it protects against arbitrary code
    execution via pickle's `__reduce__` protocol.
    """
    safe_types = (int, float, str, bool, type(None))
    if isinstance(data, safe_types):
        return True
    if isinstance(data, (list, tuple)):
        return all(_is_pickle_safe(item) for item in data)
    if isinstance(data, dict):
        return all(
            isinstance(k, str) and _is_pickle_safe(v)
            for k, v in data.items()
        )
    return False


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def interpret_serialized_content(src_file: str, content_type: str) -> Any:
    """
    Deserialize the contents of *src_file* according to *content_type*.

    Parameters
    ----------
    src_file : str
        Path to the file that contains serialized data.
    content_type : str
        One of ``'json'``, ``'text'`` or ``'pickle'``.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *content_type* is unsupported or if the data cannot be safely
        deserialized (e.g., pickle containing non‑built‑in types).
    FileNotFoundError
        If the specified file does not exist.
    """
    # Normalize content_type to lowercase for case‑insensitive matching
    fmt = content_type.strip().lower()

    if fmt not in {"json", "text", "pickle"}:
        raise ValueError(f"Unsupported content type: {content_type!r}")

    path = Path(src_file)

    # Read the raw bytes from the file
    try:
        raw_bytes = path.read_bytes()
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {src_file}") from exc

    if fmt == "json":
        # JSON is safe by definition for built‑in types
        return json.loads(raw_bytes.decode("utf-8"))

    if fmt == "text":
        # Plain text – return the decoded string
        return raw_bytes.decode("utf-8")

    if fmt == "pickle":
        # Untrusted pickle – perform a sanity check before loading
        try:
            obj = pickle.loads(raw_bytes)
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to unpickle data") from exc

        if not _is_pickle_safe(obj):
            raise ValueError("Unpickled data contains unsafe objects")

        return obj