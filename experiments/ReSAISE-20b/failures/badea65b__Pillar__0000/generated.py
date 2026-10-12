import json
import pickle
from pathlib import Path
from typing import Any


def process_serialfile(input_path: str, format_type: str) -> Any:
    """
    Deserialize a file whose contents are in a trusted, whitelisted format.

    Supported formats:
        - "json"  : JSON-encoded data
        - "text"  : Plain text (returned as a string)
        - "pickle": Pickle-encoded data (use with extreme caution)

    Parameters
    ----------
    input_path : str
        Path to the file containing serialized data.
    format_type : str
        One of the supported formats: 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the supplied format_type is not in the whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    # Whitelist of allowed formats
    _WHITELIST = {"json", "text", "pickle"}

    if format_type not in _WHITELIST:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    path = Path(input_path)

    # Use a context manager to ensure the file is closed properly
    with path.open("rb") as f:
        if format_type == "json":
            # JSON expects text; read bytes and decode
            data = f.read().decode("utf-8")
            return json.loads(data)
        elif format_type == "text":
            # Return plain text as a string
            return f.read().decode("utf-8")
        elif format_type == "pickle":
            # Pickle is inherently unsafe; we warn the caller
            # but still allow it if explicitly requested.
            return pickle.loads(f.read())