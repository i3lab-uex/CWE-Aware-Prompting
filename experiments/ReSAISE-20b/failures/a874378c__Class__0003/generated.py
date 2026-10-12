import json

# Optional: support for YAML if needed (requires PyYAML)
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

def security_content_deserializer(byte_stream: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    byte_stream : bytes
        Serialized data.
    data_format : str
        Format of the serialized data. Supported values are:
        - 'json'
        - 'yaml' (requires PyYAML)

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if not isinstance(byte_stream, (bytes, bytearray)):
        raise TypeError("byte_stream must be a bytes-like object")

    fmt = data_format.strip().lower()
    if fmt == 'json':
        try:
            text = byte_stream.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON") from exc

    if fmt == 'yaml':
        if yaml is None:
            raise ValueError("PyYAML is not installed, cannot deserialize YAML")
        try:
            text = byte_stream.decode('utf-8')
            return yaml.safe_load(text)
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ValueError("Failed to deserialize YAML") from exc

    # If we reach here, the format is not supported
    raise ValueError(f"Unsupported or insecure data format: {data_format!r}")