import json
from typing import Any

# Optional: support for safe YAML if needed
try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize `input_data` according to the specified `input_format`.

    Only a limited set of safe formats are supported:
        - 'json'   : JSON format using the standard library.
        - 'yaml'   : YAML safe load (if pyyaml is available).
    Any other format will raise a ValueError to prevent insecure deserialization.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be decoded.
    input_format : str
        Identifier of the serialization format.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes-like")

    fmt = input_format.lower()

    if fmt == "json":
        try:
            return json.loads(input_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        if yaml is None:
            raise ValueError("YAML support not available (missing PyYAML)")
        try:
            return yaml.safe_load(input_data.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise ValueError("Invalid YAML data") from exc

    # Reject all other formats to avoid insecure deserialization
    raise ValueError(f"Unsupported or unsafe format: {input_format}")