import json
import pickle
from pathlib import Path
from typing import Any, Set


# Define the whitelist of safe formats and acceptable pickle object types
_WHITELIST_FORMATS: Set[str] = {"json", "text", "pickle"}
# For pickle we only allow simple data structures to mitigate security risks
_ALLOWED_PICKLE_TYPES: Set[type] = {
    dict,
    list,
    tuple,
    set,
    str,
    int,
    float,
    bool,
    type(None),
}


def _validate_pickle_object(obj: Any) -> None:
    """
    Recursively validate that a deserialized pickle object only contains
    types from the allowed set. Raises ValueError if an unsafe type is found.
    """
    if isinstance(obj, (dict, list, tuple, set)):
        for item in obj.values() if isinstance(obj, dict) else obj:
            _validate_pickle_object(item)
    elif type(obj) not in _ALLOWED_PICKLE_TYPES:
        raise ValueError(f"Disallowed pickle object type: {type(obj).__name__}")


def process_serialfile(input_path: str, format_type: str) -> Any:
    """
    Securely deserialize data from a file.

    Parameters
    ----------
    input_path : str
        Path to the serialized file.
    format_type : str
        Format of the serialized data. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in the whitelist or if a pickle object contains disallowed types.
    FileNotFoundError
        If the input file does not exist.
    """
    # Validate format
    if format_type.lower() not in _WHITELIST_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    path = Path(input_path)
    if not path.is_file():
        raise FileNotFoundError(f"File does not exist: {input_path}")

    fmt = format_type.lower()

    if fmt == "json":
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if fmt == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()

    if fmt == "pickle":
        with path.open("rb") as f:
            data = pickle.load(f)
        # Perform a safety check on the deserialized object
        _validate_pickle_object(data)
        return data

    # Should never reach here due to whitelist check
    raise ValueError(f"Unhandled format: {format_type}")