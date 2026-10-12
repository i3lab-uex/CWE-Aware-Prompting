import json

def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialized data. Supported values:
            - 'json'  (case-insensitive)

    Returns
    -------
    object
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    fmt = data_format.lower()
    if fmt != "json":
        raise ValueError(f"Unsupported or insecure format: {data_format!r}")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc