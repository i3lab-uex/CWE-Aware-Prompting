import json

# Define a set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object for a limited set of safe formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data.
    data_format : str
        The format of the serialized data. Only formats listed in SAFE_FORMATS are allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or considered insecure.
    """
    # Normalise the format string
    fmt = data_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure data format: {data_format!r}")

    # Decode the bytes to a string (JSON is text-based)
    try:
        data_str = byte_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte stream could not be decoded using UTF-8") from exc

    # Perform the deserialization
    if fmt == "json":
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # In case more formats are added in the future, they can be handled here.