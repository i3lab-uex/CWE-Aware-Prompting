import json

# Optional: yaml may not be available in all environments. Import lazily.
try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


def deserialize_content_stream(stream: bytes, stream_format: str):
    """
    Deserialize a byte stream into a Python object.

    Only the following formats are considered safe and supported:
        - 'json': JSON format using json.loads
        - 'yaml' or 'yml': YAML format using yaml.safe_load

    Parameters:
        stream (bytes): The serialized data as bytes.
        stream_format (str): Identifier of the serialization format.

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or insecure.
        TypeError: If stream is not bytes.
    """
    if not isinstance(stream, (bytes, bytearray)):
        raise TypeError("stream must be bytes or bytearray")

    fmt = stream_format.strip().lower()
    # Decode the byte stream to a string (UTF-8 is standard for JSON/YAML)
    try:
        text = stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("stream contains invalid UTF-8 data") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("invalid JSON data") from exc

    if fmt in {"yaml", "yml"}:
        if yaml is None:
            raise ValueError("YAML support not available in this environment")
        try:
            return yaml.safe_load(text)
        except Exception as exc:  # pragma: no cover
            raise ValueError("invalid YAML data") from exc

    raise ValueError(f"Unsupported or insecure format: {stream_format}")