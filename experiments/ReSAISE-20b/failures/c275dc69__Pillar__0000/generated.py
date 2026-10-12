import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The data to deserialize.
    stream_format : str
        One of the supported, safe formats ('json').

    Returns
    -------
    object
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `stream_format` is unsupported or considered insecure.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise TypeError("serialized_data must be bytes-like")

    fmt = stream_format.lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF-8 before parsing
            decoded = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF-8 data for JSON deserialization") from exc

        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    # Add more safe formats here if needed (e.g., 'msgpack', 'yaml' with safe loader)

    raise ValueError(f"Unsupported or insecure stream format: {stream_format}")