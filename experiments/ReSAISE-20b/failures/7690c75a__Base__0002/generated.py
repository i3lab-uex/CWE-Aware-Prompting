import json

# List of formats considered safe for deserialization.
ALLOWED_FORMATS = {
    "json": _deserialize_json,
}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `data_format` is not in the list of allowed formats or if the
        deserialization fails.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    try:
        return ALLOWED_FORMATS[fmt](data)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize data with format {data_format!r}: {exc}") from exc


def _deserialize_json(data: bytes):
    """
    Deserialize JSON data. Assumes UTF‑8 encoding.

    Parameters
    ----------
    data : bytes

    Returns
    -------
    object
        The decoded Python object.

    Raises
    ------
    json.JSONDecodeError
        If the data is not valid JSON.
    """
    text = data.decode("utf-8")
    return json.loads(text)