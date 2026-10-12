import json
import pickle
from pathlib import Path
from typing import Any


# List of built‑in types that are considered safe for unpickling
SAFE_BUILTINS = {
    "builtins": {"int", "float", "str", "list", "dict", "tuple", "set",
                 "bool", "NoneType"},
}

class SafeUnpickler(pickle.Unpickler):
    """
    Unpickler that only allows a predefined set of safe built‑in types.
    Any attempt to instantiate other classes will raise an exception.
    """
    def find_class(self, module: str, name: str):
        if module in SAFE_BUILTINS and name in SAFE_BUILTINS[module]:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(
            f"Attempted to unpickle unsafe object: {module}.{name}"
        )

def load_serialized_data(filepath: str, format_type: str) -> Any:
    """
    Safely deserialize data from the given file.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    format_type : str
        One of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is unsupported or if deserialization fails.
    """
    allowed_formats = {"json", "text", "pickle"}
    if format_type not in allowed_formats:
        raise ValueError(f"Unsupported format '{format_type}'. "
                         f"Allowed formats: {', '.join(allowed_formats)}")

    path = Path(filepath)
    if not path.is_file():
        raise ValueError(f"File does not exist: {filepath}")

    try:
        if format_type == "json":
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)

        if format_type == "text":
            with path.open("r", encoding="utf-8") as f:
                return f.read()

        if format_type == "pickle":
            with path.open("rb") as f:
                return SafeUnpickler(f).load()

    except (json.JSONDecodeError, pickle.UnpicklingError,
            EOFError, ValueError) as exc:
        raise ValueError(f"Failed to deserialize file '{filepath}': {exc}") from exc