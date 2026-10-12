import json
from typing import Any

# Optional: use msgpack if available, otherwise fall back to None
try:
    import msgpack  # type: ignore[import]
except ImportError:   # pragma: no cover
    msgpack = None

# Optional: use PyYAML safe loader if available, otherwise fall back to None
try:
    import yaml  # type: ignore[import]
except ImportError:   # pragma: no cover
    yaml = None


ALLOWED_FORMATS = {
    "json",
    "msgpack",   # optional, if msgpack is installed
    "yaml",      # optional, if yaml is installed
}

def _json_deserialize(stream: bytes) -> Any:
    """Deserialize JSON data from a byte stream."""
    text = stream.decode("utf-8")
    return json.loads(text)

def _msgpack_deserialize(stream: bytes) -> Any:
    """Deserialize MessagePack data from a byte stream."""
    if msgpack is None:  # pragma: no cover
        raise RuntimeError("msgpack library is not installed")
    return msgpack.unpackb(stream, raw=False)

def _yaml_deserialize(stream: bytes) -> Any:
    """Deserialize YAML data from a byte stream using safe_load."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError("yaml library is not installed")
    text = stream.decode("utf-8")
    return yaml.safe_load(text)


_DESERIALIZERS = {
    "json": _json_deserialize,
    "msgpack": _msgpack_deserialize,
    "yaml": _yaml_deserialize,
}


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    whitelisted, secure formats.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    serialization_format : str
        Format of the serialized data. Must be one of 'json', 'msgpack',
        or 'yaml' (if the corresponding library is available).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    RuntimeError
        If a required library for an allowed format is missing.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported serialization format '{serialization_format}'. "
            "Allowed formats are: json, msgpack (if available), yaml (if available)."
        )

    deserializer = _DESERIALIZERS.get(fmt)
    if deserializer is None:
        # This can happen if the format was added to ALLOWED_FORMATS but its
        # deserializer function is missing (e.g., optional dependency not installed).
        raise RuntimeError(f"No deserializer implemented for format '{serialization_format}'")

    try:
        return deserializer(stream)
    except Exception as exc:  # pragma: no cover
        # Wrap any exception to avoid leaking implementation details.
        raise ValueError(f"Failed to deserialize stream: {exc}") from exc