import json
import pickle
from pathlib import Path
from typing import Any


class SafeUnpickler(pickle.Unpickler):
    """
    A custom Unpickler that only allows safe built‑in types.
    All other classes raise a pickle.UnpicklingError.
    """
    _allowed_classes = {
        (list, tuple, dict, set, frozenset, str, bytes, int, float, bool, type(None)),
    }

    def find_class(self, module: str, name: str):
        # Only allow built-in types
        if module == "builtins":
            cls = getattr(pickle.builtins, name)
            if cls in self._allowed_classes:
                return cls
        raise pickle.UnpicklingError(
            f"Disallowed class {module}.{name} during unpickling"
        )


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load and deserialize data from a file using only trusted formats.

    Parameters
    ----------
    filepath : str
        Path to the serialized file.
    data_format : str
        The serialization format. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist.
    """
    allowed_formats = {"json", "text", "pickle"}
    fmt = data_format.lower()
    if fmt not in allowed_formats:
        raise ValueError(f"Untrusted or unsupported format: {data_format}")

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    if fmt == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if fmt == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    if fmt == "pickle":
        with path.open("rb") as f:
            return SafeUnpickler(f).load()