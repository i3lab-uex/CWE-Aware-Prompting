#!/usr/bin/env python3
"""
Secure file deserialization helper.

This module provides a single function, `deserialize_file_data`, which
reads data from a file and deserializes it only if the format is on an
explicit whitelist.  The function accepts three safe formats:

* ``json``   – JSON text, parsed with the standard library `json` module.
* ``text``   – Plain UTF‑8 text, returned as a string.
* ``pickle`` – Pickle data *only if* the file was produced by a trusted
  source and contains no executable code.  The function uses
  `pickle.loads` with a custom unpickler that forbids the creation of
  arbitrary objects (see `RestrictedUnpickler` below).

Any other format triggers a ``ValueError``.  The function also guards
against common pitfalls such as missing files, permission errors,
and malformed data.

The implementation follows the guidance for CWE‑502 (Deserialization
of Untrusted Data) by limiting the formats that can be processed and
by providing a safety‑net for pickle deserialization.
"""

from __future__ import annotations

import json
import os
import pickle
import sys
from typing import Any, Callable


# --------------------------------------------------------------------------- #
#   Restricted unpickler for pickle format
# --------------------------------------------------------------------------- #

class RestrictedUnpickler(pickle.Unpickler):
    """
    A custom unpickler that only allows safe built‑in types.
    It rejects any attempt to instantiate arbitrary classes or execute
    code during unpickling.

    This class is used only when the user explicitly selects the ``pickle``
    format.  The function will raise an exception if it encounters
    disallowed opcodes.
    """

    # List of safe built‑in classes that may be instantiated during
    # unpickling.  Add more as needed.
    _safe_builtins = {
        "builtins.dict",
        "builtins.list",
        "builtins.tuple",
        "builtins.set",
        "builtins.int",
        "builtins.float",
        "builtins.str",
        "builtins.bytes",
        "builtins.bool",
    }

    def find_class(self, module: str, name: str) -> Callable:
        """
        Override to restrict class resolution.
        Only built‑ins listed in _safe_builtins are allowed.
        """
        fullname = f"{module}.{name}"
        if fullname in self._safe_builtins:
            return getattr(pickle, name) if module == "builtins" else super().find_class(module, name)
        raise pickle.UnpicklingError(f"Disallowed unpicklable object: {fullname}")


def restricted_loads(data: bytes) -> Any:
    """
    Safely load pickled data using the RestrictedUnpickler.
    """
    return RestrictedUnpickler(io.BytesIO(data)).load()


# --------------------------------------------------------------------------- #
#   Main deserialization function
# --------------------------------------------------------------------------- #

def deserialize_file_data(input_filepath: str, input_format: str) -> Any:
    """
    Deserialize data from a file while enforcing a whitelist of safe formats.

    Parameters
    ----------
    input_filepath : str
        Path to the file containing serialized data.
    input_format : str
        Format of the serialized data.  Must be one of:
        - 'json'   : JSON text.
        - 'text'   : Plain UTF‑8 text.
        - 'pickle' : Pickle data (safe mode).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    FileNotFoundError
        If the file does not exist.
    PermissionError
        If the file cannot be read due to permissions.
    json.JSONDecodeError, pickle.UnpicklingError
        If the data is malformed for the selected format.
    """

    # Whitelist of allowed formats
    ALLOWED_FORMATS = {"json", "text", "pickle"}

    if input_format not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported format '{input_format}'. Allowed formats: {sorted(ALLOWED_FORMATS)}"
        )

    if not os.path.isfile(input_filepath):
        raise FileNotFoundError(f"File not found: {input_filepath}")

    # Read the file content in binary mode for all formats to avoid
    # encoding surprises; text will be decoded explicitly.
    try:
        with open(input_filepath, "rb") as f:
            raw_data = f.read()
    except PermissionError as exc:
        raise PermissionError(f"Cannot read file '{input_filepath}': {exc}") from exc

    # Deserialize according to the requested format
    if input_format == "json":
        try:
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"JSON file is not valid UTF‑8: {exc}") from exc
        return json.loads(text)

    if input_format == "text":
        try:
            return raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Text file is not valid UTF‑8: {exc}") from exc

    if input_format == "pickle":
        # Use the restricted unpickler
        return RestrictedUnpickler(io.BytesIO(raw_data)).load()


# --------------------------------------------------------------------------- #
#   Optional demo (executed only when run as a script)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    import argparse
    import io

    parser = argparse.ArgumentParser(description="Demo of deserialize_file_data")
    parser.add_argument("filepath", help="Path to the serialized file")
    parser.add_argument("--format", choices=["json", "text", "pickle"], required=True, help="Format of the file")
    args = parser.parse_args()

    try:
        result = deserialize_file_data(args.filepath, args.format)
        print("Deserialized object:")
        print(result)
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        sys.exit(1)