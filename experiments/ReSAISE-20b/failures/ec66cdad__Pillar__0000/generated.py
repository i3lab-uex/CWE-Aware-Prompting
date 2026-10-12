import json

# A set of serialization formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data to be deserialized.
    serialization_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested serialization type is not in ALLOWED_FORMATS.
    """
    if serialization_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization type: {serialization_type}")

    # Only JSON is supported at this time.
    if serialization_type.lower() == "json":
        try:
            # JSON expects text; decode bytes to str using UTF-8.
            decoded_text = byte_data.decode("utf-8")
            return json.loads(decoded_text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc