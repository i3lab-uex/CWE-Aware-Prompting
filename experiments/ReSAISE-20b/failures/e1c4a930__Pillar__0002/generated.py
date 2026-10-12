import json

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object for a limited set of safe formats.

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
        If the format is unsupported or deemed insecure.
    """
    # Normalize the format string to avoid case‑sensitivity issues
    fmt = data_format_type.strip().lower()

    # Only allow explicitly listed safe formats.
    if fmt != 'json':
        raise ValueError(f"Unsupported or insecure format: {data_format_type!r}")

    # Convert bytes to string using UTF‑8; if decoding fails, raise a clear error.
    try:
        text = serialized_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8 encoded JSON") from exc

    # Parse the JSON string safely.
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc