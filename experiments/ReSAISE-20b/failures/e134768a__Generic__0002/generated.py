import json

# Define a set of safe, supported formats for deserialization.
SAFE_FORMATS = {"json"}

def unpack_serialized_object(byte_data: bytes, struct_format: str):
    """
    Deserialize binary data from a trusted source.

    Parameters
    ----------
    byte_data : bytes
        The serialized binary data.
    struct_format : str
        Format identifier used for deserialization (e.g., 'json').

    Returns
    -------
    object
        The Python object produced by deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS.
    TypeError
        If byte_data is not a bytes-like object.
    json.JSONDecodeError
        If the data cannot be decoded as JSON.
    """
    if not isinstance(byte_data, (bytes, bytearray)):
        raise TypeError("byte_data must be a bytes-like object")

    if struct_format not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    # For JSON we assume UTF‑8 encoding.
    text = byte_data.decode("utf-8")
    return json.loads(text)