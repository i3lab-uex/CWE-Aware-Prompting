import json
from typing import Any

# Optional: support for YAML if PyYAML is available.
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Only safe, predefined formats are accepted. Unsupported or unsafe
    formats raise a ValueError.

    Parameters:
        stream (bytes): The serialized byte stream.
        serialization_format (str): Format identifier, e.g. 'json', 'yaml'.

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or unsafe.
    """
    if not isinstance(stream, (bytes, bytearray)):
        raise TypeError("stream must be bytes or bytearray")

    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            text = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON stream is not valid UTF‑8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available (missing PyYAML)")
        try:
            text = stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("YAML stream is not valid UTF‑8") from exc
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:  # type: ignore
            raise ValueError("Failed to decode YAML") from exc

    # Add more safe formats here as needed.

    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")