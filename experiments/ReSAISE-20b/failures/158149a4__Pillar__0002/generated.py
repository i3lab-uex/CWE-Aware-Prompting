import json
import pickle
from pathlib import Path
from typing import Any


def load_serialized_data(filepath: str, format_type: str) -> Any:
    """
    Safely deserialize data from a file.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    format_type : str
        Serialization format. Must be one of the trusted formats:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of approved formats.
    FileNotFoundError
        If `filepath` does not exist.
    """
    # Define the whitelist of allowed formats
    _ALLOWED_FORMATS = {"json", "text", "pickle"}

    if format_type not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}")

    file_path = Path(filepath)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {filepath!r}")

    # Open the file in the appropriate mode
    if format_type == "text":
        mode = "r"
    else:  # json or pickle
        mode = "rb"

    with file_path.open(mode) as f:
        if format_type == "json":
            # json is safe by design
            return json.load(f)
        elif format_type == "text":
            # Return the raw string
            return f.read()
        else:  # pickle
            # NOTE: Pickle is inherently unsafe. This function should only be used
            # with data from a fully trusted source. The following line performs
            # the deserialization, but users should be aware of the security risks.
            return pickle.load(f)