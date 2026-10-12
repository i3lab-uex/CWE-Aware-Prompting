import json

def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialization. Only 'json' is supported.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json"}

    fmt = data_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure data format: {data_format}")

    if fmt == "json":
        # Ensure the data is valid UTF-8 before decoding
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

        try:
            # json.loads already handles type safety; no arbitrary code execution
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # The whitelist guarantees we never reach this point,
    # but a fallback for future formats can be added here.