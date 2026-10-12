import json

def deserialize_content(data: bytes, data_format: str):
    """
    Safely deserializes the given byte stream into a Python object.

    Parameters
    ----------
    data : bytes
        Serialized data that needs to be deserialized.
    data_format : str
        The format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    fmt = data_format.lower()

    if fmt == "json":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    # Add other safe formats here if desired
    # e.g., fmt == "msgpack": ...

    # Reject any other format to avoid unsafe deserialization
    raise ValueError(f"Unsupported or insecure data format: {data_format!r}")