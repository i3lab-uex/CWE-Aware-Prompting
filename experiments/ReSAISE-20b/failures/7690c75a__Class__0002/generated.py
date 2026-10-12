import json
from typing import Any

try:
    import yaml  # optional dependency; used only for safe YAML loading
except ImportError:  # pragma: no cover
    yaml = None


def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Format of the serialized data. Supported formats are:
        - 'json'
        - 'yaml' (only if ``pyyaml`` is installed)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or unsafe.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available (pyyaml missing)")
        try:
            return yaml.safe_load(data.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ValueError("Invalid YAML data") from exc

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported data format: {data_format!r}")