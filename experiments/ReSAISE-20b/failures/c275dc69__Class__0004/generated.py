import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object while restricting
    to safe, predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The serialized data to be deserialized.
    stream_format : str
        Identifier of the serialization format. Only 'json' is allowed.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    # Normalize format string to lower case
    fmt = stream_format.lower()

    if fmt != "json":
        raise ValueError(
            f"Unsupported or insecure format '{stream_format}'. "
            "Only 'json' is allowed."
        )

    # Decode bytes to string (JSON expects text)
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

    # Parse the JSON string
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Data is not valid JSON") from exc