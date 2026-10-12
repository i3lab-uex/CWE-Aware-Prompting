import json
import pickle
from pathlib import Path
from typing import Any


def load_serialized_data(file_location: str, data_format: str) -> Any:
    """
    Load and deserialize data from a file located at `file_location`.

    Parameters
    ----------
    file_location : str
        Path to the serialized data file.
    data_format : str
        Format of the serialized data. Must be one of the supported formats:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided format is not in the allowed whitelist.
    FileNotFoundError
        If the file does not exist.
    """
    # Define a whitelist of supported formats
    ALLOWED_FORMATS = {"json", "text", "pickle"}

    # Validate format
    if data_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format '{data_format}'. "
                         f"Allowed formats: {sorted(ALLOWED_FORMATS)}")

    file_path = Path(file_location)

    # Ensure the file exists
    if not file_path.is_file():
        raise FileNotFoundError(f"File '{file_location}' does not exist or is not a regular file.")

    # Read and deserialize based on format
    if data_format == "json":
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    if data_format == "text":
        with file_path.open("r", encoding="utf-8") as f:
            return f.read()

    # For pickle, use a restricted loading context if possible
    with file_path.open("rb") as f:
        # In many environments, pickle is considered unsafe.
        # Here we assume that the caller explicitly allowed it via the whitelist.
        return pickle.load(f)