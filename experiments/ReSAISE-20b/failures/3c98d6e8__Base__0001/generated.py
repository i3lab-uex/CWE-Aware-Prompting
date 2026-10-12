import json
import pickle
from pathlib import Path
from typing import Any


def load_serial_data(f_path: str, f_format: str) -> Any:
    """
    Deserialize data from a file whose format is guaranteed to be trusted.

    Parameters
    ----------
    f_path : str
        Path to the file containing the serialized data.
    f_format : str
        Format of the serialized data. Must be one of the whitelisted options:
        'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If `f_format` is not in the whitelist of safe formats.
    FileNotFoundError
        If the file does not exist or cannot be accessed.
    """
    # Whitelist of trusted formats
    allowed_formats = {"json", "text", "pickle"}

    if f_format not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe format '{f_format}'. "
                         f"Allowed formats: {', '.join(sorted(allowed_formats))}")

    file_path = Path(f_path)

    if not file_path.is_file():
        raise FileNotFoundError(f"File '{f_path}' does not exist or is not a regular file.")

    # Use binary mode for pickle, text mode otherwise
    if f_format == "pickle":
        with file_path.open("rb") as fp:
            return pickle.load(fp)
    else:  # json or text
        with file_path.open("r", encoding="utf-8") as fp:
            if f_format == "json":
                return json.load(fp)
            else:  # text
                return fp.read()