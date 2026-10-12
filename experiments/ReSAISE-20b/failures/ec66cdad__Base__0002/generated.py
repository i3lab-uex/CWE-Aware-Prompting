import json

# Define a whitelist of safe serialization formats.
ALLOWED_SERIALIZATIONS = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized stream of data.
    serialization_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    object
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the serialization_type is not in the allowed list or if deserialization fails.
    """
    # Normalise and validate the requested format
    fmt = serialization_type.strip().lower()
    if fmt not in ALLOWED_SERIALIZATIONS:
        raise ValueError(f"Unsupported or unsafe serialization type: {serialization_type!r}")

    try:
        if fmt == "json":
            # JSON is text-based, so decode the bytes first
            decoded = byte_data.decode("utf-8")
            return json.loads(decoded)
    except Exception as exc:
        # Wrap any exception in a ValueError to avoid leaking internal details
        raise ValueError(f"Deserialization failed for type {serialization_type!r}: {exc}") from None