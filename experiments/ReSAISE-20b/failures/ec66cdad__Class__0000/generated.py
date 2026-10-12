import json

# List of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Deserialize a byte stream into a Python object using only allowed formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested serialization_type is not in ALLOWED_FORMATS.
    """
    # Normalise format string
    fmt = serialization_type.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization type: '{serialization_type}'")

    if fmt == "json":
        # Decode bytes to text before parsing
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte data could not be decoded as UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # The function should never reach here because all allowed formats are handled.
    raise ValueError(f"Unhandled serialization type: '{serialization_type}'")