import json

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize `data_bytes` into a Python object using the specified
    serialization format. Only trusted formats are allowed to avoid
    executing arbitrary code.

    Parameters
    ----------
    data_bytes : bytes
        The serialized object in byte format.
    format_name : str
        Name of the serialization format. Supported values are:
            'json' - JSON data encoded in UTF‑8.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `format_name` is not one of the supported formats.
    """
    if format_name.lower() != 'json':
        raise ValueError(f"Unsupported or unsafe format: {format_name!r}")

    try:
        # JSON expects text, so decode bytes as UTF‑8 first.
        json_text = data_bytes.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8 encoded JSON") from exc

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc