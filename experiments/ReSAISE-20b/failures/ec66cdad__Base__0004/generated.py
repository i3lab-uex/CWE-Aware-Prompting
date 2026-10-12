import json
import yaml  # safe loader only

# Define the set of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {
    'json': json.loads,
    # yaml.safe_load is explicitly safe; it does not construct arbitrary Python objects.
    'yaml': yaml.safe_load,
}

def restore_object_from_stream(byte_data: bytes, serialization_type: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        Format of the serialized data. Only 'json' and 'yaml'
        are accepted.

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe serialization format is requested,
        or if deserialization fails.
    """
    # Normalise the type string and check against allowed formats
    fmt = serialization_type.strip().lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization type: {serialization_type}")

    # Retrieve the appropriate deserializer
    deserializer = ALLOWED_FORMATS[fmt]

    try:
        # For json and yaml, the input must be a string.
        data_str = byte_data.decode('utf-8')
    except Exception as exc:
        raise ValueError("Failed to decode byte stream as UTF-8") from exc

    try:
        return deserializer(data_str)
    except Exception as exc:
        raise ValueError(f"Deserialization failed for format '{serialization_type}': {exc}") from exc