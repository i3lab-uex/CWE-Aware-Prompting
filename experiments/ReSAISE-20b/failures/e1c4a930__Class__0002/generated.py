import json

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object for supported formats.

    Supported formats:
        - 'json': JSON encoded data

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or deemed insecure.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise ValueError("serialized_data must be bytes or bytearray")

    fmt = data_format_type.strip().lower()
    if fmt == "json":
        # JSON is safe for deserialization as it only produces basic data types
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode bytes as UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # All other formats are considered unsafe or unsupported
    raise ValueError(f"Unsupported or insecure format: {data_format_type}")