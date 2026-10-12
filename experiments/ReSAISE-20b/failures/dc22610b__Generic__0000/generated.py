import json
import pickle
from pathlib import Path

# Whitelisted formats considered safe for deserialization.
WHITELISTED_FORMATS = {"json", "text", "pickle"}


def handle_serialized_file(serialized_file_path: str, serialization_format: str):
    """
    Deserialize data from a file using only trusted formats.

    Parameters
    ----------
    serialized_file_path : str
        Path to the file containing serialized data.
    serialization_format : str
        Format of the serialized data. Must be one of:
            'json'   - JSON text
            'text'   - Plain UTF‑8 text
            'pickle' - Pickle objects (only if trusted source)

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in WHITELISTED_FORMATS.
    FileNotFoundError
        If the file does not exist.
    """
    if serialization_format not in WHITELISTED_FORMATS:
        raise ValueError(
            f"Untrusted or unsupported serialization format: {serialization_format!r}"
        )

    path = Path(serialized_file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {serialized_file_path}")

    # Read the raw bytes or text based on format
    if serialization_format == "text":
        content = path.read_text(encoding="utf-8")
        return content

    raw_bytes = path.read_bytes()

    if serialization_format == "json":
        # JSON deserialization is safe for plain data structures.
        return json.loads(raw_bytes.decode("utf-8"))

    # For pickle, we assume the source is trusted. Use a restricted
    # Unpickler if you want to mitigate certain attacks.
    return pickle.loads(raw_bytes)