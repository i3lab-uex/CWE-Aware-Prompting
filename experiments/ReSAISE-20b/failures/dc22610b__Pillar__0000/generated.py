import json
import pickle
from pathlib import Path
from typing import Any

# Whitelisted serialization formats that are considered safe for this context.
SAFE_FORMATS = {"json", "text", "pickle"}


def handle_serialized_file(
    serialized_file_path: str, serialization_format: str
) -> Any:
    """
    Deserialize data from a file while ensuring that only trusted formats are processed.

    Parameters
    ----------
    serialized_file_path : str
        Path to the file containing serialized data.
    serialization_format : str
        The format of the serialized data. Must be one of 'json', 'text', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the supplied format is not in the whitelist of safe formats.
    FileNotFoundError
        If the file does not exist or cannot be accessed.
    """
    # Ensure the format is one of the approved safe formats
    if serialization_format not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or untrusted serialization format: {serialization_format}"
        )

    file_path = Path(serialized_file_path)

    # Use a context manager to guarantee the file is closed properly,
    # preventing resource leakage (CWE‑664).
    with file_path.open("rb") as fh:
        if serialization_format == "json":
            # JSON requires text mode; read bytes and decode.
            data_bytes = fh.read()
            try:
                return json.loads(data_bytes.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                raise ValueError("Failed to decode JSON data") from exc

        elif serialization_format == "text":
            # Return the raw string content.
            try:
                return fh.read().decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("Failed to decode text data") from exc

        elif serialization_format == "pickle":
            # Pickle is inherently unsafe; use only if explicitly whitelisted.
            try:
                return pickle.loads(fh.read())
            except (pickle.UnpicklingError, EOFError) as exc:
                raise ValueError("Failed to unpickle data") from exc

    # This line should never be reached because all supported formats are handled above.
    raise ValueError("Unhandled serialization format.")