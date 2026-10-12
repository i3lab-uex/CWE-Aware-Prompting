import json

def deserialize_stream(serialized_data: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream to be deserialized.
    stream_format : str
        One of the supported format identifiers. Currently only 'json' is allowed.

    Returns
    -------
    object
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(serialized_data, bytes):
        raise TypeError("serialized_data must be of type 'bytes'")

    fmt = stream_format.lower()
    if fmt == "json":
        try:
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON data: {exc}") from exc
    else:
        raise ValueError(f"Unsupported or insecure format '{stream_format}'. "
                         "Only 'json' is allowed.")