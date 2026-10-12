import json

# A whitelist of safe formats for deserialization.
SAFE_FORMATS = {
    'json': json.loads,
}

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object for supported formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        The format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    # Normalise the format string
    fmt = data_format_type.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: '{data_format_type}'")

    try:
        # Decode bytes to str using UTF-8, the default for JSON
        text = serialized_data.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError("Input data is not valid UTF-8") from e

    # Perform deserialization using the safe loader
    try:
        return SAFE_FORMATS[fmt](text)
    except Exception as e:  # Catch all exceptions from the loader
        raise ValueError("Deserialization failed") from e