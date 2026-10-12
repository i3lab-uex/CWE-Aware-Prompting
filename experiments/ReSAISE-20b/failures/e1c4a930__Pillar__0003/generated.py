import json

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object for a limited set of safe formats.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream containing the serialized data.
    data_format_type : str
        A string identifying the format of the serialized data. Only supported values are:
        - 'json' : JSON encoded data.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format type is not supported or the data cannot be decoded.
    """
    if not isinstance(serialized_data, bytes):
        raise ValueError("serialized_data must be of type 'bytes'")

    # Strip leading/trailing whitespace for safety
    cleaned = serialized_data.strip()

    if data_format_type.lower() == "json":
        try:
            text = cleaned.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode bytes as UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON payload") from exc

    # Add more safe formats here if needed in the future.
    raise ValueError(f"Unsupported or insecure format: {data_format_type!r}")