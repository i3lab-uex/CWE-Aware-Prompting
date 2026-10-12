import json

# A set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Deserialize a byte stream into a Python object using only allowed formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization type is not supported or considered unsafe.
    """
    if serialization_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_type}")

    # For JSON, decode bytes to string and load.
    try:
        if serialization_type.lower() == "json":
            # Decode assuming UTF-8; ignore errors to avoid crashes on malformed data.
            text = byte_data.decode("utf-8", errors="strict")
            return json.loads(text)
    except Exception as exc:
        # Wrap any deserialization exception in ValueError to keep a consistent API.
        raise ValueError(f"Failed to deserialize data as {serialization_type}") from exc