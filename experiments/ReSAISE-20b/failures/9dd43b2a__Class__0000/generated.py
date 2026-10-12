import json

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object only if the format is trusted.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if not isinstance(content, bytes):
        raise ValueError("content must be a bytes object")

    format_type = format_type.lower()
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Currently only JSON is supported.
    try:
        return json.loads(content.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError("Failed to deserialize content") from exc