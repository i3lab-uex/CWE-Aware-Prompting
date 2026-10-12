import json

# List of formats that are considered safe for deserialization
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
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(content, (bytes, bytearray)):
        raise ValueError("Content must be bytes or bytearray.")

    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    if fmt == "json":
        try:
            # JSON expects text, so decode using UTF-8
            return json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to parse JSON content") from exc

    # Future safe formats can be added here
    raise ValueError(f"Unhandled safe format: {format_type}")