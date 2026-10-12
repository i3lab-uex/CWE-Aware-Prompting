import json

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe,
    pre-approved formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Format of the serialized data. Currently only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the list of allowed formats.
    """
    # Define a whitelist of safe, supported formats
    ALLOWED_FORMATS = {
        'json': _deserialize_json,
        # Future safe formats can be added here
    }

    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    return ALLOWED_FORMATS[fmt](data)


def _deserialize_json(data: bytes):
    """
    Safely deserialize JSON data from bytes.

    Parameters
    ----------
    data : bytes
        UTF‑8 encoded JSON byte string.

    Returns
    -------
    Any
        The Python object represented by the JSON data.
    """
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 for JSON deserialization") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc