import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream to be deserialized.
    stream_format : str
        Identifier of the serialization format. Only 'json' is supported.

    Returns
    -------
    object
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `stream_format` is not supported or considered insecure.
    """
    # Define the set of safe, allowed formats
    SAFE_FORMATS = {
        'json': _deserialize_json,
    }

    format_key = stream_format.lower()
    if format_key not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure stream format: '{stream_format}'")

    return SAFE_FORMATS[format_key](serialized_data)


def _deserialize_json(data: bytes):
    """
    Deserialize JSON data from a byte stream.

    Parameters
    ----------
    data : bytes
        Byte representation of JSON-encoded data.

    Returns
    -------
    object
        The Python object represented by the JSON data.
    """
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data must be UTF-8 encoded") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc