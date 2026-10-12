import json
from typing import Any

# Optional: safe yaml and msgpack imports. They are imported lazily
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

try:
    import msgpack  # type: ignore
except ImportError:
    msgpack = None


def deserialize_content_stream(stream: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    stream_format : str
        Format of the serialized data. Supported formats are:
            - 'json'   : JSON (using json.loads)
            - 'yaml'   : YAML safe load (requires PyYAML)
            - 'msgpack': MessagePack (requires msgpack)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or required library is missing.
    """
    fmt = stream_format.lower()

    if fmt == "json":
        try:
            # json.loads expects a str; decode using UTF-8
            return json.loads(stream.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available: PyYAML is not installed.")
        try:
            return yaml.safe_load(stream.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ValueError("Invalid YAML data") from exc

    if fmt == "msgpack":
        if msgpack is None:
            raise ValueError("MessagePack support not available: msgpack is not installed.")
        try:
            return msgpack.unpackb(stream, raw=False)
        except (msgpack.ExtraData, msgpack.FormatError) as exc:
            raise ValueError("Invalid MessagePack data") from exc

    # If we reach here, the format is not supported
    raise ValueError(f"Unsupported or insecure format: {stream_format}")