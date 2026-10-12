import json

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object only if the format is safe.

    Parameters
    ----------
    stream : bytes
        The serialized data to be deserialized.
    stream_format : str
        The format of the serialized data. Supported values are defined in
        `SAFE_FORMATS`. Any other value will raise a ValueError.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in SAFE_FORMATS.
    """
    # Normalise and validate the format string
    fmt = stream_format.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: '{stream_format}'")

    # Only 'json' is supported in this safe implementation
    if fmt == "json":
        try:
            # Decode the bytes to a string using UTF-8 (common for JSON)
            text = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Stream is not valid UTF-8 encoded JSON") from exc

        # json.loads will safely parse the JSON string into Python objects
        return json.loads(text)

    # The following line is unreachable because SAFE_FORMATS contains only 'json',
    # but it keeps the function future‑proof if new safe formats are added.
    raise ValueError(f"Deserialization for format '{stream_format}' is not implemented.")