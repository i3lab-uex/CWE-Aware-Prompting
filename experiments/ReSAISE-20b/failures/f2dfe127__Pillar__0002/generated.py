import json

# A whitelist of serialization formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json": json.loads,
}

def bytes_to_obj(data_bytes: bytes, format_name: str):
    """
    Deserialize data from raw bytes into a Python object using a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        Serialized representation of the object.
    format_name : str
        The name of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist of safe formats.
    """
    # Normalise the format name (case‑insensitive) and look it up in the whitelist.
    fmt = format_name.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format '{format_name}'. Only the following formats are allowed: {', '.join(SAFE_FORMATS)}")

    # Decode bytes to a string. The encoding is assumed to be UTF‑8 which is standard for JSON.
    try:
        text = data_bytes.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded using UTF‑8") from exc

    # Call the corresponding safe deserializer.
    return SAFE_FORMATS[fmt](text)