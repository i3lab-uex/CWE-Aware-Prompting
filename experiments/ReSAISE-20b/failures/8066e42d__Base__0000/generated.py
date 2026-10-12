import json
import pickle
from pathlib import Path
from typing import Any

__all__ = ["deserialize_file_data"]

# Define the list of serialization formats that are considered safe
SAFE_FORMATS = {"json", "text", "pickle"}


def deserialize_file_data(filepath: str, serialization_format: str) -> Any:
    """
    Deserialize data from a file in a secure manner.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    serialization_format : str
        The format of the serialized data. Must be one of the trusted formats:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The Python object obtained by deserializing the file contents.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS.
    FileNotFoundError
        If the file does not exist.
    OSError
        For other I/O errors (e.g., permission denied).
    """
    if serialization_format not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{serialization_format}'. "
            f"Allowed formats: {sorted(SAFE_FORMATS)}"
        )

    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Read file contents
    if serialization_format == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    else:
        # For json and pickle we read bytes to avoid any encoding issues
        with path.open("rb") as f:
            data = f.read()

    if serialization_format == "json":
        # json.loads expects a str, so decode bytes safely
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 data in JSON file: {exc}") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Failed to parse JSON: {exc}") from exc

    if serialization_format == "pickle":
        # Pickle is inherently unsafe; however, the caller has explicitly
        # opted into this format.  We still catch errors to provide clear feedback.
        try:
            return pickle.loads(data)
        except (pickle.UnpicklingError, EOFError) as exc:
            raise ValueError(f"Failed to unpickle data: {exc}") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization format: {serialization_format}")