import json
import pickle
from pathlib import Path
from typing import Any


# ------------------------------------------------------------------
# Restricted unpickler to mitigate CWE‑502
# ------------------------------------------------------------------
class RestrictedUnpickler(pickle.Unpickler):
    """
    A pickle Unpickler that only allows safe, built‑in types.
    All other classes will be replaced with a generic placeholder.
    """

    # Allowed built‑in types that are considered safe
    SAFE_BUILTINS = {
        'list',
        'tuple',
        'dict',
        'set',
        'frozenset',
        'str',
        'bytes',
        'int',
        'float',
        'bool',
        'NoneType',
    }

    def find_class(self, module: str, name: str):
        if module == 'builtins' and name in self.SAFE_BUILTINS:
            return getattr(__import__(module), name)
        # Reject any other class by raising an exception
        raise pickle.UnpicklingError(
            f"Attempt to load unsafe class {module}.{name}"
        )


def restricted_loads(data: bytes) -> Any:
    """
    Safely load pickled data using RestrictedUnpickler.
    """
    return RestrictedUnpickler(io.BytesIO(data)).load()


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def process_serialfile(input_path: str, format_type: str) -> Any:
    """
    Deserialize a file safely according to the specified format.

    Parameters
    ----------
    input_path : str
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
        If an unsupported or untrusted format is requested.
    FileNotFoundError, PermissionError, etc.
        Propagated from file I/O operations.
    """
    allowed_formats = {"json", "text", "pickle"}
    fmt = format_type.lower()
    if fmt not in allowed_formats:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    path = Path(input_path)
    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {input_path}")

    content = path.read_bytes()

    if fmt == "json":
        # json.loads expects a string; decode bytes using utf‑8
        return json.loads(content.decode("utf-8"))
    elif fmt == "text":
        # Plain text: return the decoded string
        return content.decode("utf-8")
    elif fmt == "pickle":
        # Use restricted unpickler
        return RestrictedUnpickler(io.BytesIO(content)).load()
    # The following line is unreachable due to the whitelist check
    raise ValueError(f"Unhandled format: {format_type}")