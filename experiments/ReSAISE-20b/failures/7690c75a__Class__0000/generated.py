import json

# List of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only approved formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    if data_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    # Currently only JSON is supported.
    try:
        text = data.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Data could not be decoded as UTF-8: {exc}") from exc

    try:
        return json.loads(text)
    except Exception as exc:
        raise ValueError(f"JSON deserialization failed: {exc}") from exc