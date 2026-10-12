import json

# Define a mapping of supported, safe formats to their deserialization functions.
# Only JSON is considered safe for arbitrary data structures from untrusted sources.
SUPPORTED_FORMATS = {
    "json": json.loads,
}

def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    data_format : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the requested format is unsupported or considered insecure.
    """
    # Normalise format string: strip whitespace, lower-case
    fmt = data_format.strip().lower()

    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported or insecure deserialization format: '{data_format}'")

    # For JSON, the input must be a UTF‑8 encoded string.
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8 encoded JSON") from exc

    # Use the corresponding deserializer
    try:
        return SUPPORTED_FORMATS[fmt](text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ValueError("Failed to deserialize data") from exc