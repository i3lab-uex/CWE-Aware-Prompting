import json
import yaml  # PyYAML provides a safe loader
from typing import Any

def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `data` according to the specified `data_format`.

    Supported formats:
        - 'json': JSON format, safe by default.
        - 'yaml': YAML format using PyYAML's safe_load.
        - 'msgpack': MessagePack format via the `msgpack` library (optional).
    Unsupported or insecure formats raise ValueError.

    Args:
        data: The serialized byte stream.
        data_format: Identifier of the serialization format.

    Returns:
        Python object represented by `data`.

    Raises:
        ValueError: If the format is unsupported or insecure.
        TypeError: If `data` is not a bytes-like object.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    fmt = data_format.lower()
    try:
        if fmt == "json":
            # JSON expects a text string; decode using UTF-8
            return json.loads(data.decode("utf-8"))
        elif fmt == "yaml":
            # YAML can contain arbitrary objects; use safe_load
            return yaml.safe_load(data.decode("utf-8"))
        elif fmt == "msgpack":
            try:
                import msgpack
            except ImportError as exc:
                raise ValueError("msgpack support not available") from exc
            # msgpack.unpackb is safe for standard types when use_list=False
            return msgpack.unpackb(data, raw=False)
        else:
            # Disallow pickle and other potentially unsafe formats
            raise ValueError(f"Unsupported or insecure data format: {data_format}")
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ValueError(f"Failed to deserialize data for format '{data_format}': {exc}") from exc