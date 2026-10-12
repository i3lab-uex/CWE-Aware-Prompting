import json

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object.

    Only the JSON format is considered safe for untrusted input.
    All other formats raise a ValueError.

    Args:
        serialized_data: The data to deserialize, as bytes.
        data_format_type: A string indicating the format of the data
                          (e.g. 'json', 'pickle').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or insecure.
        json.JSONDecodeError: If JSON data is malformed.
    """
    if not isinstance(serialized_data, bytes):
        raise TypeError("serialized_data must be of type 'bytes'")

    fmt = data_format_type.lower()
    if fmt == "json":
        # Decode bytes to string using UTF-8, then parse JSON
        text = serialized_data.decode("utf-8")
        return json.loads(text)
    else:
        raise ValueError(f"Unsupported or insecure format: {data_format_type}")