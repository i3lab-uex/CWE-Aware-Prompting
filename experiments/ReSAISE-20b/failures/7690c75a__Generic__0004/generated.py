import json

__all__ = ["decode_data_stream"]

# A set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Format of the serialized data (e.g., 'json').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_format` is not in the list of allowed formats.
    TypeError
        If `data` is not a bytes-like object or if the data cannot be decoded.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be a bytes-like object")

    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    if fmt == "json":
        # JSON expects a text string, so decode bytes using UTF-8.
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise TypeError("data could not be decoded as UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # In case new safe formats are added in the future, handle them here.
    raise ValueError(f"Unhandled data format: {data_format!r}")