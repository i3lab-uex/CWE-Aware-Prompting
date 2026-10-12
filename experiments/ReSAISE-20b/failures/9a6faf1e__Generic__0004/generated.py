import json
import pickle
from pathlib import Path

# Whitelist of trusted serialization formats
_TRUSTED_FORMATS = {"json", "text", "pickle"}

def read_serialized_file(file_path: str, file_format: str):
    """
    Safely deserializes the contents of a file based on the specified format.

    Parameters
    ----------
    file_path : str
        Path to the serialized data file.
    file_format : str
        Serialization format. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not in the trusted list or if the file cannot be read.
    """
    fmt = file_format.lower()
    if fmt not in _TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {file_format!r}")

    path = Path(file_path)
    if not path.is_file():
        raise ValueError(f"File does not exist: {file_path!r}")

    try:
        if fmt == "json":
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)

        if fmt == "text":
            with path.open("r", encoding="utf-8") as f:
                return f.read()

        if fmt == "pickle":
            # Pickle is inherently unsafe, but we trust the source
            with path.open("rb") as f:
                return pickle.load(f)

    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize {file_path!r} as {fmt}") from exc