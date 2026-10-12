import json

# Only the following formats are considered safe for deserialization.
SAFE_FORMATS = {
    'json': json.loads,
}

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream containing the serialized data.
    data_format_type : str
        The format of the serialized data. Supported values are:
        - 'json'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if data_format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format_type!r}")

    # Decode bytes to a string using UTF-8, which is the standard for JSON.
    try:
        text = serialized_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Failed to decode bytes as UTF-8") from exc

    # Perform deserialization using the safe parser.
    try:
        return SAFE_FORMATS[data_format_type](text)
    except Exception as exc:
        # Wrap any exception that occurs during parsing.
        raise ValueError("Deserialization failed") from exc