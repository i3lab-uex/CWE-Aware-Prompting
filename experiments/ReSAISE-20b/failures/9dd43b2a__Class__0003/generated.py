import json

# Define the list of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object for trusted formats only.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g. 'json').

    Returns
    -------
    object
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(content, bytes):
        raise TypeError("content must be a bytes object")

    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Currently only JSON is supported as a safe format.
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Content is not valid UTF-8 encoded JSON") from exc

    try:
        return json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc