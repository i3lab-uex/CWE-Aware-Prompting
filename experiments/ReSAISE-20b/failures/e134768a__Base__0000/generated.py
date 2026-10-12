import json

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json": json.loads,
}

def unpack_serialized_object(byte_data: bytes, struct_format: str):
    """
    Deserialize binary data from an untrusted source using only
    predefined safe formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to be deserialized.
    struct_format : str
        Identifier of the serialization format. Supported values are:
        - 'json'

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is not in SAFE_FORMATS or if deserialization fails.
    """
    # Ensure the requested format is supported
    if struct_format not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{struct_format}'. "
            f"Allowed formats: {', '.join(SAFE_FORMATS.keys())}"
        )

    # Retrieve the appropriate deserializer
    deserializer = SAFE_FORMATS[struct_format]

    try:
        # For JSON, we need to decode bytes into a string
        if struct_format == "json":
            text = byte_data.decode("utf-8")
            return deserializer(text)
        # Extend here for additional formats if needed
    except Exception as exc:
        raise ValueError(f"Deserialization error for format '{struct_format}': {exc}") from exc