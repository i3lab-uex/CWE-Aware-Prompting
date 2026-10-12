import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The data to deserialize.
    stream_format : str
        Format of the serialized data. Supported formats are:
            * 'json'  – JSON format (safe, no code execution).

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(serialized_data, bytes):
        raise TypeError("serialized_data must be of type 'bytes'")

    # Normalize format string
    fmt = stream_format.strip().lower()

    if fmt == "json":
        # JSON is safe because it only represents basic data structures
        return json.loads(serialized_data.decode("utf-8"))
    else:
        # Any other format is rejected to avoid unsafe deserialization
        raise ValueError(f"Unsupported or insecure stream format: {stream_format}")