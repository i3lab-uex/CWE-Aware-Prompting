import json

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str):
    """
    Deserialize `content` based on the specified `format_type`.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of supported and secure formats.
    """
    # Normalize format type to lower case for comparison
    fmt = format_type.lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Currently only JSON is supported
    if fmt == "json":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Content is not valid UTF-8 encoded JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # If more formats are added in the future, they should be handled here
    raise ValueError(f"Format handler for '{format_type}' is not implemented")