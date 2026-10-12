import json

# A whitelist of safe, supported serialization formats.
ALLOWED_FORMATS = {
    "json": json.loads,
}

def decode_data_stream(data: bytes, data_format: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data : bytes
        The serialized byte stream to be deserialized.
    data_format : str
        The format of the serialized data. Only formats in ``ALLOWED_FORMATS`` are permitted.

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If ``data_format`` is not in the whitelist of safe formats.
    """
    # Normalise the format string to lower case to avoid accidental mismatches
    fmt = data_format.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    # Convert bytes to string if necessary
    try:
        payload = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data must be valid UTF‑8 for JSON deserialization") from exc

    # Perform the actual deserialization
    try:
        return ALLOWED_FORMATS[fmt](payload)
    except Exception as exc:  # pragma: no cover
        # Wrap any exception to avoid leaking internal details
        raise ValueError(f"Failed to deserialize data: {exc}") from exc