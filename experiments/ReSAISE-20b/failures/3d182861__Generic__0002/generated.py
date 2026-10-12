import json

def deserialize_content(data: bytes, data_format: str):
    """
    Safely deserializes a byte stream into a Python object.

    Parameters
    ----------
    data : bytes
        The serialized data that needs to be deserialized.
    data_format : str
        A string indicating the deserialization format (e.g., 'json').

    Returns
    -------
    object
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    # Only allow a small set of safe formats
    allowed_formats = {"json"}

    fmt_lower = data_format.lower()
    if fmt_lower not in allowed_formats:
        raise ValueError(f"Unsupported or insecure data format: {data_format}")

    if fmt_lower == "json":
        # Decode bytes to string, then parse JSON
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF‑8 encoded JSON") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # This line should never be reached due to the allowed_formats check,
    # but is kept for completeness.
    raise ValueError(f"Unhandled data format: {data_format}")