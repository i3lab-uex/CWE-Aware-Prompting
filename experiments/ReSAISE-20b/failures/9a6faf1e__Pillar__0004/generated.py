import json
import pickle
from pathlib import Path
from typing import Any


def read_serialized_file(file_path: str, file_format: str) -> Any:
    """
    Safely deserialize the contents of a file.

    Parameters
    ----------
    file_path : str
        Path to the serialized data file.
    file_format : str
        Serialization format. Must be one of the trusted formats:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist or if
        deserialization fails.
    FileNotFoundError
        If ``file_path`` does not exist.
    """
    # Whitelist of safe formats
    _ALLOWED_FORMATS = {"json", "text", "pickle"}

    if file_format not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {file_format!r}")

    path = Path(file_path)
    # Ensure the file exists before attempting to open
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {file_path}")

    # Open the file using a context manager to guarantee closure
    with path.open("rb") as fh:
        raw_data = fh.read()

    try:
        if file_format == "json":
            # Decode bytes to str before json.loads
            text = raw_data.decode("utf-8")
            return json.loads(text)
        elif file_format == "text":
            # Return the raw text string
            return raw_data.decode("utf-8")
        elif file_format == "pickle":
            # Pickle is included in the whitelist, but still
            # handle errors gracefully.
            return pickle.loads(raw_data)
    except Exception as exc:
        raise ValueError(f"Failed to deserialize {file_format!r} data: {exc}") from exc