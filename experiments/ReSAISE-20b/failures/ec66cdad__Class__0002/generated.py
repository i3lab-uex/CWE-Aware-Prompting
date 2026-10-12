import json

# Allowed formats for deserialization.
ALLOWED_FORMATS = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    serialization_type : str
        Format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or considered unsafe.
    """
    # Normalise type string (case-insensitive).
    fmt = serialization_type.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization type: {serialization_type}")

    # For JSON we expect a UTF‑8 encoded byte stream.
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF‑8 for JSON") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to decode JSON data") from exc