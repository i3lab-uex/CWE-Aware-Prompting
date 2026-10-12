import json

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object for supported and secure formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        The format type of the serialized data. Supported values are:
            - 'json'

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Only allow explicitly whitelisted formats
    supported_formats = {'json'}

    fmt = data_format_type.lower()
    if fmt not in supported_formats:
        raise ValueError(f"Unsupported or insecure format: {data_format_type}")

    # Decode bytes to string safely
    try:
        text = serialized_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Serialized data is not valid UTF-8.") from exc

    # Use json.loads for safe deserialization
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse JSON data.") from exc