import json

# --------------------------------------------------------------------------- #
# Secure deserialization helper
# --------------------------------------------------------------------------- #

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Safely deserializes a byte stream into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The data to deserialize.
    stream_format : str
        One of the supported, safe formats: 'json'.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Normalize format name to lowercase for case-insensitive matching
    fmt = stream_format.lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF-8 (common encoding)
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF-8 data for JSON format: {exc}") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed JSON data: {exc}") from exc

    # Add more safe formats here if needed, e.g. 'msgpack', 'cbor2', etc.

    # If we reach this point, the format is not supported or considered unsafe
    raise ValueError(f"Unsupported or insecure stream format: {stream_format}")