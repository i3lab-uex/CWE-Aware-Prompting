import json

def deserialize_content(data: bytes, data_format: str):
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    data : bytes
        The serialized data that needs to be deserialized.
    data_format : str
        A string indicating the deserialization format (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {
        'json': json.loads,
    }

    fmt_lower = data_format.lower()
    if fmt_lower not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    # Decode the bytes to a string (UTF‑8 is safe for JSON)
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8 encoded text") from exc

    # Perform the deserialization
    loader = SAFE_FORMATS[fmt_lower]
    try:
        return loader(text)
    except Exception as exc:
        # Wrap any exception from the deserializer in ValueError
        raise ValueError(f"Failed to deserialize data: {exc}") from exc