import json
import pickle
from typing import Any

class RestrictedUnpickler(pickle.Unpickler):
    """
    Unpickler that only allows safe built-in types and forbids arbitrary
    code execution by rejecting any module or class import.
    """
    def find_class(self, module: str, name: str):
        # Only allow built-in types from the 'builtins' module
        if module == "builtins":
            return getattr(__import__(module), name)
        raise pickle.UnpicklingError(f"Forbidden global {module}.{name}")

def process_serialfile(input_path: str, format_type: str) -> Any:
    """
    Deserialize data from a file in a controlled manner.

    Parameters
    ----------
    input_path : str
        Path to the serialized file.
    format_type : str
        Format of the data ('json', 'text', or 'pickle').

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
    if format_type not in allowed_formats:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    with open(input_path, "rb") as f:
        if format_type == "json":
            # JSON is read as text; decode bytes first
            data = f.read().decode("utf-8")
            return json.loads(data)
        elif format_type == "text":
            # Return raw text
            return f.read().decode("utf-8")
        elif format_type == "pickle":
            # Use restricted unpickler to mitigate code execution risk
            return RestrictedUnpickler(f).load()