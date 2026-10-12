import json
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream.
    serialization_format : str
        The format of the serialized data. Supported formats are:
            * 'json'  - JSON format (safe).
            * 'yaml'  - YAML format using yaml.safe_load (if available).

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested, or if deserialization fails.
    """
    if not isinstance(stream, (bytes, bytearray)):
        raise ValueError("Stream must be bytes or bytearray")

    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            text = stream.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available (PyYAML missing)")
        try:
            text = stream.decode("utf-8")
            return yaml.safe_load(text)
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ValueError(f"YAML deserialization error: {exc}") from exc

    # If we reach here, the format is unsupported
    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")