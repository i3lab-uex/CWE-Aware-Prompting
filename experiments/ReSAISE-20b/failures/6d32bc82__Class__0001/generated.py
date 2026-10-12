import json

# Define a set of serialization formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def deserialize_stream_data(stream: bytes, serialization_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data stream.
    serialization_format : str
        A string indicating the format of the serialized data. Only formats listed in
        `ALLOWED_FORMATS` are permitted.

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `serialization_format` is not in the list of allowed formats.
    """
    # Normalize format string to lower case for comparison
    fmt = serialization_format.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: '{serialization_format}'")

    # Currently only JSON is supported.  Convert the bytes to a string and parse.
    if fmt == "json":
        try:
            text = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Stream could not be decoded as UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("JSON deserialization failed") from exc

    # If additional formats are added in the future, they should be handled
    # explicitly here.  The default case is unreachable because of the
    # earlier membership check, but is kept for completeness.
    raise ValueError(f"Unhandled format: '{serialization_format}'")