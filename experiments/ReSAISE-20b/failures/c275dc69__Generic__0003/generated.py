import json
from typing import Any

# Optional: use yaml if available and safe
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def deserialize_stream(serialized_data: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using a restricted set of formats.

    Parameters
    ----------
    serialized_data : bytes
        The data to deserialize.
    stream_format : str
        One of the supported formats: 'json', optionally 'yaml' if PyYAML is installed.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise TypeError("serialized_data must be bytes or bytearray")

    fmt = stream_format.lower()

    if fmt == "json":
        try:
            return json.loads(serialized_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available (PyYAML not installed)")
        try:
            return yaml.safe_load(serialized_data.decode("utf-8"))
        except (yaml.YAMLError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid YAML data") from exc

    # All other formats are considered insecure or unsupported
    raise ValueError(f"Unsupported or insecure format: {stream_format}")