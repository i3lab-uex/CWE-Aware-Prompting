import json
from typing import Any

# Only these formats are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using a safe, predefined format.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream.
    serialization_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    # Only JSON is supported; decode bytes to str and load.
    try:
        text = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Stream is not valid UTF-8") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc