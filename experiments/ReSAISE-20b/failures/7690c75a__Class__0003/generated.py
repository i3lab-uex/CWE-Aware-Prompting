import json

# Only these formats are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    if data_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format}")

    # At this point we know the format is safe (currently only JSON).
    try:
        # Decode bytes to string before parsing.
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse JSON data") from exc