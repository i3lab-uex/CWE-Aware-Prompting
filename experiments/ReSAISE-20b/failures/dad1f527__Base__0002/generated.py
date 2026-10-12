#!/usr/bin/env python3
"""
Secure deserialization helper.

Supported formats:
    - json   : JSON text (safe)
    - text   : plain UTF‑8 text
    - pickle : Python pickle, but only if it contains safe built‑in types.
"""

import json
import pickle
from pathlib import Path
from typing import Any


class RestrictedUnpickler(pickle.Unpickler):
    """
    Unpickler that only allows loading of safe built‑in types.
    Any attempt to instantiate a custom class or module raises an exception.
    """
    SAFE_BUILTINS = {
        'builtins',
        'int', 'float', 'str', 'bool', 'bytes', 'list', 'tuple',
        'dict', 'set', 'frozenset', 'NoneType'
    }

    def find_class(self, module: str, name: str):
        if (module, name) in {('builtins', n) for n in self.SAFE_BUILTINS}:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(
            f"Disallowed pickle object: {module}.{name}"
        )


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load and deserialize data from *filepath* using the specified *data_format*.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    data_format : str
        One of 'json', 'text', or 'pickle'.  Other values raise ValueError.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If *data_format* is not in the whitelist.
    FileNotFoundError, OSError
        If the file cannot be accessed.
    json.JSONDecodeError
        For malformed JSON data.
    pickle.UnpicklingError
        If the pickle payload contains disallowed objects or is malformed.
    """
    allowed_formats = {'json', 'text', 'pickle'}
    fmt = data_format.lower()
    if fmt not in allowed_formats:
        raise ValueError(f"Unsupported or untrusted format: {data_format!r}")

    path = Path(filepath)
    if fmt == 'json':
        with path.open('rt', encoding='utf-8') as f:
            return json.load(f)
    elif fmt == 'text':
        with path.open('rt', encoding='utf-8') as f:
            return f.read()
    else:  # pickle
        with path.open('rb') as f:
            return RestrictedUnpickler(f).load()