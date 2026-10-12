import json

# Define the list of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The serialization format of the content. Only formats listed in
        SAFE_FORMATS are accepted.

    Returns
    -------
    Any
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in SAFE_FORMATS or if deserialization fails.
    """
    # Normalise the format string to lower case for comparison
    fmt = format_type.lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Currently only JSON is supported
    try:
        # Decode bytes to string using UTF-8 (JSON requires text)
        decoded = content.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode content: {exc}") from exc

    try:
        return json.loads(decoded)
    except Exception as exc:
        raise ValueError(f"JSON deserialization error: {exc}") from exc