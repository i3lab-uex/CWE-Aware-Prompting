import json

try:
    import yaml  # Optional dependency for YAML support
except ImportError:  # pragma: no cover - optional
    yaml = None


def deserialize_content(data: bytes, data_format: str):
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The format of the serialization. Supported values are:
        - 'json'
        - 'yaml' (requires PyYAML)
        Any other value will raise a ValueError.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure, or if required dependencies are missing.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError("Data must be bytes-like")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available (missing PyYAML)")
        try:
            return yaml.safe_load(data.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ValueError("Invalid YAML data") from exc

    # Disallow other formats (e.g., pickle, marshal, etc.) for security
    raise ValueError(f"Unsupported or insecure data format: {data_format}")