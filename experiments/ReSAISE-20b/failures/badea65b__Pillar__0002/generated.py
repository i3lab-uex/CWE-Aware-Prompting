import json
import pickle
from pathlib import Path

__all__ = ["process_serialfile"]

# Whitelist of safe formats
SAFE_FORMATS = {"json", "text"}

def process_serialfile(input_path: str, format_type: str):
    """
    Deserialize data from a file using only trusted formats.

    Parameters
    ----------
    input_path : str
        Path to the serialized file.
    format_type : str
        The serialization format of the data. Must be one of
        ``"json"``, ``"text"``, or optionally ``"pickle"`` if the user
        explicitly trusts the source.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if an unsupported
        format_type is provided.
    """
    # Normalise the format string and validate it
    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS and fmt != "pickle":
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    path = Path(input_path)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {input_path}")

    # Use a context manager to ensure the file is closed properly
    with path.open("rb") as fh:
        data = fh.read()

    # Dispatch based on the format
    if fmt == "json":
        try:
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if fmt == "text":
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode text data") from exc

    # ``pickle`` is included only if explicitly requested
    if fmt == "pickle":
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as exc:
            raise ValueError("Failed to unpickle data") from exc

    # This point should never be reached due to earlier validation
    raise ValueError(f"Unhandled format: {format_type}")