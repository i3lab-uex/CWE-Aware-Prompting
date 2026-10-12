import json
import pickle
from pathlib import Path
from typing import Any

# Whitelisted formats that are considered safe for deserialization
SAFE_FORMATS = {"json", "text", "pickle"}

# Basic types that we consider safe to expose after deserialization
ALLOWED_TYPES = (
    dict,
    list,
    tuple,
    str,
    int,
    float,
    bool,
    type(None),
)


def _validate_deserialized(obj: Any) -> None:
    """
    Ensure the deserialized object is of a simple, safe type.
    Raises ValueError if an unsafe type is encountered.
    """
    # For sequences, validate each element recursively
    if isinstance(obj, (list, tuple)):
        for item in obj:
            _validate_deserialized(item)
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if not isinstance(key, (str, int, float, bool)):
                raise ValueError(f"Unsafe dict key type: {type(key).__name__}")
            _validate_deserialized(value)
    elif not isinstance(obj, ALLOWED_TYPES):
        raise ValueError(f"Unsafe deserialized type: {type(obj).__name__}")


def handle_serialized_file(
    serialized_file_path: str, serialization_format: str
) -> Any:
    """
    Deserialize a file that contains data in one of the whitelisted formats.
    Only simple, safe Python objects are returned; complex or malicious
    structures will raise a ValueError.

    Parameters
    ----------
    serialized_file_path : str
        Path to the file containing serialized data.
    serialization_format : str
        The format of the serialized data. Must be one of 'json', 'text',
        or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not whitelisted or if deserialization yields an unsafe object.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {serialization_format}")

    path = Path(serialized_file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {serialized_file_path}")

    if fmt == "json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    elif fmt == "text":
        with path.open("r", encoding="utf-8") as f:
            data = f.read()
    elif fmt == "pickle":
        with path.open("rb") as f:
            data = pickle.load(f)
    else:  # This block is unreachable due to the whitelist check
        raise ValueError(f"Unsupported format: {serialization_format}")

    # Validate that the deserialized data is safe
    _validate_deserialized(data)

    return data