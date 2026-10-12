import json

def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Deserialization format. Currently only 'json' is supported.

    Returns
    -------
    object
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `data_format` is unsupported or considered insecure.
    """
    # Only allow JSON for safety
    if data_format.lower() != 'json':
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    try:
        # JSON expects text, so decode using UTF-8
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

    try:
        # Use json.loads to safely parse the JSON string
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc