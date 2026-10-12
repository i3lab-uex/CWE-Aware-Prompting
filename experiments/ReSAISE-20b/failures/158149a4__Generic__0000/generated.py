import json
import pickle
from pathlib import Path
from typing import Any


def load_serialized_data(filepath: str, format_type: str) -> Any:
    """
    Securely deserialize data from a file in an approved format.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    format_type : str
        Serialization format. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not supported or considered unsafe.
    FileNotFoundError
        If the file does not exist.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json", "text", "pickle"}

    if format_type not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{format_type}'. "
            f"Allowed formats: {', '.join(sorted(SAFE_FORMATS))}"
        )

    path = Path(filepath)

    if not path.is_file():
        raise FileNotFoundError(f"No such file: '{filepath}'")

    # Use binary mode for JSON and pickle to avoid encoding issues
    if format_type == "json":
        with path.open("rb") as f:
            return json.load(f)
    elif format_type == "text":
        with path.open("r", encoding="utf-8") as f:
            return f.read()
    elif format_type == "pickle":
        # Pickle is inherently unsafe; only allow if explicitly requested.
        with path.open("rb") as f:
            return pickle.load(f)