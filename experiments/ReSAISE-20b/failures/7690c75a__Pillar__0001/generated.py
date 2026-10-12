import json

# Define a whitelist of safe serialization formats.
ALLOWED_FORMATS = {
    'json': json.loads,
}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, whitelisted formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the specified format is not in the allowed list or if deserialization fails.
    """
    # Normalise the format string
    fmt = data_format.strip().lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    # Decode bytes to string (JSON requires text)
    try:
        text = data.decode('utf-8')
    except Exception as exc:
        raise ValueError("Data could not be decoded as UTF‑8") from exc

    # Perform deserialization
    try:
        return ALLOWED_FORMATS[fmt](text)
    except Exception as exc:
        raise ValueError("Deserialization failed") from exc