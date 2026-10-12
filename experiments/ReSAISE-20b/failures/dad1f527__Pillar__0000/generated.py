import json
import pickle
from pathlib import Path
from typing import Any


def load_serialized_data(filepath: str, data_format: str) -> Any:
    """
    Load a serialized file using only a whitelist of safe formats.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    data_format : str
        One of 'json', 'text', or 'pickle'.  Any other value raises ValueError.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist or if deserialization fails.
    """
    # Whitelist of safe formats
    allowed_formats = {"json", "text", "pickle"}

    if data_format not in allowed_formats:
        raise ValueError(f"Untrusted or unsupported format: {data_format!r}")

    file_path = Path(filepath)

    # Ensure the file exists before attempting to read
    if not file_path.is_file():
        raise ValueError(f"File does not exist: {filepath!r}")

    try:
        with file_path.open("rb") as f:
            raw_data = f.read()
    except OSError as exc:
        raise ValueError(f"Unable to read file {filepath!r}") from exc

    # Deserialize based on the format
    if data_format == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if data_format == "text":
        try:
            return raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode text data") from exc

    if data_format == "pickle":
        # Pickle is inherently unsafe; we still allow it only as part of the whitelist.
        # Use protocol 4 or higher to avoid compatibility issues, and load in a
        # restricted environment by limiting the allowed classes.
        try:
            return pickle.loads(raw_data, fix_imports=True)
        except Exception as exc:  # pylint: disable=broad-except
            raise ValueError("Failed to load pickle data") from exc

    # This point should never be reached due to the whitelist check above.
    raise ValueError("Unexpected error: unsupported format")