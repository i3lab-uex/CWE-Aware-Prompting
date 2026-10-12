import json
import pickle
from typing import Any, Iterable


class SafeUnpickler(pickle.Unpickler):
    """
    A restricted unpickler that only allows loading of built‑in types.
    Any attempt to load a custom class or module will raise an exception.
    """

    def find_class(self, module: str, name: str) -> Any:
        # Only allow built‑in modules that expose simple data types
        allowed_modules = {"builtins"}
        if module not in allowed_modules:
            raise pickle.UnpicklingError(
                f"Attempted to load disallowed module '{module}'."
            )
        # For builtins, only allow a whitelist of safe types
        allowed_builtins = {
            "list",
            "tuple",
            "dict",
            "set",
            "frozenset",
            "int",
            "float",
            "str",
            "bytes",
            "bool",
            "NoneType",
        }
        if name not in allowed_builtins:
            raise pickle.UnpicklingError(
                f"Attempted to load disallowed built‑in type '{name}'."
            )
        return getattr(__import__(module), name)


def handle_serialized_file(
    serialized_file_path: str, serialization_format: str
) -> Any:
    """
    Deserialize a file containing data in one of the supported safe formats.

    Parameters
    ----------
    serialized_file_path : str
        Path to the file containing serialized data.
    serialization_format : str
        One of 'json', 'text', or 'pickle'. The format must be in the whitelist.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided format is not in the whitelist.
    pickle.UnpicklingError
        If the pickle data contains disallowed types or modules.
    json.JSONDecodeError
        If the JSON is malformed.
    """
    # Whitelist of allowed formats
    ALLOWED_FORMATS = {"json", "text", "pickle"}

    if serialization_format not in ALLOWED_FORMATS:
        raise ValueError(
            f"Untrusted or unsupported format '{serialization_format}'. "
            "Allowed formats are: json, text, pickle."
        )

    if serialization_format == "json":
        with open(serialized_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    if serialization_format == "text":
        with open(serialized_file_path, "r", encoding="utf-8") as f:
            return f.read()

    if serialization_format == "pickle":
        with open(serialized_file_path, "rb") as f:
            # Use the safe unpickler to load only trusted types
            return SafeUnpickler(f).load()