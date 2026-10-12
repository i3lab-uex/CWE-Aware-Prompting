import json
import pickle
from pathlib import Path

# Whitelisted formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "text", "pickle"}

def handle_serialized_file(serialized_file_path: str, serialization_format: str):
    """
    Safely deserialize data from a file based on the provided format.

    Parameters
    ----------
    serialized_file_path : str
        Path to the file containing serialized data.
    serialization_format : str
        One of 'json', 'text', or 'pickle'. Any other value raises ValueError.

    Returns
    -------
    object
        The deserialized Python object (dict/list for json, str for text,
        or any pickled object if 'pickle' is chosen).

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS.
    FileNotFoundError
        If the file does not exist or cannot be accessed.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported serialization format: {serialization_format}")

    path = Path(serialized_file_path)
    data_bytes = path.read_bytes()

    try:
        if fmt == "json":
            # JSON is text; decode bytes to str before loading
            return json.loads(data_bytes.decode("utf-8"))
        elif fmt == "text":
            # Return plain text as a string
            return data_bytes.decode("utf-8")
        elif fmt == "pickle":
            # Pickle is inherently unsafe; only allow if format explicitly requested
            return pickle.loads(data_bytes)
    except Exception as exc:
        # Wrap any deserialization error in a ValueError for consistency
        raise ValueError(f"Failed to deserialize data: {exc}") from exc