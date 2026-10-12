import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using a restricted set of formats.

    Parameters
    ----------
    serialized_data : bytes
        The data to be deserialized.
    stream_format : str
        The format of the serialized data. Only 'json' is supported for security reasons.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If `stream_format` is not supported or considered insecure.
    """
    if stream_format.lower() != "json":
        raise ValueError(
            f"Unsupported or insecure format '{stream_format}'. "
            "Only 'json' is allowed."
        )

    try:
        # JSON data should be UTF‑8 encoded text
        decoded = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8 encoded JSON") from exc

    try:
        return json.loads(decoded)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc