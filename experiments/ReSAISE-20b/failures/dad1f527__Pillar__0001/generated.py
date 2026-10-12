import json
import pickle
from pathlib import Path
from typing import Any


class RestrictedUnpickler(pickle.Unpickler):
    """
    A safe unpickler that only allows loading built‑in types and simple containers.
    It rejects any class or function objects to mitigate code execution risks.
    """
    SAFE_BUILTINS = {
        "list", "tuple", "dict", "set",
        "frozenset", "str", "bytes", "bytearray",
        "int", "float", "bool", "NoneType"
    }

    def find_class(self, module: str, name: str):
        if module == "builtins" and name in self.SAFE_BUILTINS:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(f"Attempted to load unsafe class {module}.{name}")


def _safe_load_pickle(file_obj) -> Any:
    """Load pickle data using the RestrictedUnpickler."""
    return RestrictedUnpickler(file_obj).load()


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load and deserialize data from a file safely.

    Parameters
    ----------
    filepath : str
        Path to the serialized data file.
    data_format : str
        One of 'json', 'text', or 'pickle'.  Only these formats are allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the allowed whitelist or if deserialization fails.
    """
    # Whitelist of safe formats
    ALLOWED_FORMATS = {"json", "text", "pickle"}

    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {data_format!r}")

    path = Path(filepath)
    if not path.is_file():
        raise ValueError(f"File does not exist: {filepath!r}")

    # Use a context manager to ensure the file descriptor is closed
    try:
        with path.open("rb") as f:
            if fmt == "json":
                # JSON must be decoded to text before loading
                try:
                    data = f.read().decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise ValueError("JSON file is not valid UTF-8") from exc
                return json.loads(data)

            if fmt == "text":
                # Treat as plain text; decode to string
                try:
                    return f.read().decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise ValueError("Text file is not valid UTF-8") from exc

            if fmt == "pickle":
                # Use the restricted unpickler
                return _safe_load_pickle(f)

    except (json.JSONDecodeError, pickle.UnpicklingError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc