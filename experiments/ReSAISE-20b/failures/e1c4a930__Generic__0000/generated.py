import json

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object only for supported and secure formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(serialized_data, bytes):
        raise TypeError("serialized_data must be of type 'bytes'")

    fmt = data_format_type.lower()

    if fmt == "json":
        try:
            # decode bytes to str using UTF-8 before parsing
            return json.loads(serialized_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc
    else:
        # Only 'json' is considered safe in this implementation.
        raise ValueError(f"Unsupported or insecure data format: {data_format_type}")