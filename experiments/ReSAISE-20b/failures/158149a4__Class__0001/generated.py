import json
import pickle
from typing import Any

# List of trusted serialization formats
SAFE_FORMATS = {"json", "text", "pickle"}

class SafeUnpickler(pickle.Unpickler):
    """
    A custom Unpickler that only allows basic built‑in types to be instantiated.
    This mitigates the risk of executing arbitrary code during unpickling.
    """
    # Allowed built‑in types that can be constructed
    _allowed_builtins = {
        "list",
        "dict",
        "str",
        "bytes",
        "int",
        "float",
        "bool",
        "NoneType",
    }

    def find_class(self, module: str, name: str):
        # Only allow built‑in types from the 'builtins' module
        if module == "builtins" and name in self._allowed_builtins:
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(f"Attempted to instantiate unsafe class {module}.{name}")

def load_serialized_data(filepath: str, format_type: str) -> Any:
    """
    Securely load data from a file based on the specified serialization format.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    format_type : str
        Serialization format; must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in the list of trusted formats.
    """
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {format_type!r}")

    with open(filepath, "rb") as f:
        if format_type == "json":
            # JSON files are text; decode to str before loading
            return json.load(f)
        elif format_type == "text":
            # Return the file content as a string
            return f.read().decode("utf-8")
        elif format_type == "pickle":
            # Use the safe unpickler to prevent arbitrary code execution
            return SafeUnpickler(f).load()
        else:
            # This branch should never be reached due to the earlier check
            raise ValueError(f"Unhandled format: {format_type!r}")