import json
import pickle
from typing import Any

def deserialize_file_data(filepath: str, serialization_format: str) -> Any:
    """
    Securely deserializes data from a file.

    Parameters
    ----------
    filepath : str
        Path to the file containing serialized data.
    serialization_format : str
        One of the approved formats: 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is unsupported or considered unsafe.
    FileNotFoundError, OSError
        Propagated if the file cannot be opened or read.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json", "text", "pickle"}

    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    # Use a context manager to ensure the file is closed properly,
    # mitigating CWE-664 by guaranteeing resource release.
    try:
        if fmt == "json":
            # JSON is safe for deserialization
            with open(filepath, mode="r", encoding="utf-8") as f:
                return json.load(f)

        if fmt == "text":
            # Plain text: read as a string
            with open(filepath, mode="r", encoding="utf-8") as f:
                return f.read()

        if fmt == "pickle":
            # Pickle is inherently unsafe; it is only allowed here because
            # the caller explicitly requested it. The user must trust the source.
            with open(filepath, mode="rb") as f:
                return pickle.load(f)

    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to decode JSON: {exc}") from exc
    except pickle.UnpicklingError as exc:
        raise ValueError(f"Failed to unpickle data: {exc}") from exc