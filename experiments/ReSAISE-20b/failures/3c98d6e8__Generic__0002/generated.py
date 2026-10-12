import json
import pickle
from pathlib import Path
from typing import Any

def load_serial_data(f_path: str, f_format: str) -> Any:
    """
    Load and deserialize data from a file safely.

    Parameters
    ----------
    f_path : str
        Path to the serialized data file.
    f_format : str
        Format of the serialized data. Must be one of:
            'json'   - JSON format
            'text'   - Plain text (string)
            'pickle' - Pickle format (trusted only)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or considered unsafe.
    FileNotFoundError
        If the file does not exist.
    """
    allowed_formats = {"json", "text", "pickle"}

    if f_format not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe format: {f_format!r}")

    path = Path(f_path)

    if not path.is_file():
        raise FileNotFoundError(f"No such file: {f_path!r}")

    if f_format == "text":
        # Plain text – read as UTF‑8 string
        with path.open("r", encoding="utf-8") as fp:
            return fp.read()

    if f_format == "json":
        # JSON – safe parsing
        with path.open("r", encoding="utf-8") as fp:
            return json.load(fp)

    if f_format == "pickle":
        # Pickle – only use when source is trusted.
        with path.open("rb") as fp:
            return pickle.load(fp)