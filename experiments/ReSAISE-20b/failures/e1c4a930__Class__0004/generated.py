import json

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}

def deserialize_stream_payload(serialized_data: bytes, data_format_type: str):
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        Identifier of the serialization format (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object corresponding to the provided data format.

    Raises
    ------
    ValueError
        If the specified `data_format_type` is not supported or considered unsafe.
    TypeError
        If `serialized_data` is not of type bytes.
    """
    # Validate input types
    if not isinstance(serialized_data, bytes):
        raise TypeError("serialized_data must be a bytes object")

    # Normalize format string
    fmt = data_format_type.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure data format: {data_format_type!r}")

    # Safe deserialization for JSON
    if fmt == "json":
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON payload could not be decoded as UTF-8") from exc
        return json.loads(text)

    # The following block is unreachable due to SAFE_FORMATS, but kept for future expansion
    raise ValueError(f"Unhandled safe format: {fmt!r}")