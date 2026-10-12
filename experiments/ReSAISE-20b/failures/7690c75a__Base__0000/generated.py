import json

# Only these formats are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If `data_format` is not among the allowed formats, or if the data
        cannot be parsed according to that format.
    """
    # Normalise format string (case‑insensitive)
    fmt = data_format.strip().lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    try:
        if fmt == "json":
            # JSON is text based; decode bytes to str before parsing.
            return json.loads(data.decode("utf-8"))
    except Exception as exc:
        # Wrap any parsing exception into a ValueError to keep the API
        # consistent and avoid leaking implementation details.
        raise ValueError(f"Failed to deserialize data as {data_format!r}: {exc}") from exc