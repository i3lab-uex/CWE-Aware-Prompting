import json

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object only for approved formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data to be deserialized.
    data_format : str
        Identifier of the serialization format. Supported values are:
            - 'json'  (default, safe)

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or considered insecure.
    """
    # Normalize format string to lower case
    fmt = data_format.strip().lower()

    if fmt == 'json':
        try:
            # Decode bytes to str using UTF-8 before json.loads
            text = byte_stream.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Byte stream is not valid UTF-8 for JSON deserialization") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # Add more safe formats here if needed, e.g. 'msgpack', 'yaml.safe_load', etc.
    # For now only JSON is considered safe.

    raise ValueError(f"Unsupported or insecure data format: {data_format!r}")