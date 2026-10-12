import json

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object using only supported, secure formats.

    Supported formats:
        - 'json': JSON format (text-based and safe when parsed with json.loads).

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream containing the serialized data.
    data_format_type : str
        A string indicating the format of the serialized data.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Normalise format string to lowercase for comparison
    fmt = data_format_type.strip().lower()

    if fmt == "json":
        # JSON expects a text string; decode using UTF-8 (common default)
        try:
            decoded_text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 encoded JSON data: {exc}") from exc

        # Parse the JSON safely
        try:
            return json.loads(decoded_text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed JSON data: {exc}") from exc

    # Add additional safe formats here in the future, e.g.
    # elif fmt == "msgpack":
    #     import msgpack
    #     return msgpack.loads(serialized_data)

    # Unsupported or insecure format
    raise ValueError(f"Unsupported or unsafe data format: '{data_format_type}'")