import json
from typing import Any

# Only these formats are considered safe for deserialization.
SAFE_FORMATS = {"json", "yaml"}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize `content` according to the specified `format_type`.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        Format of the serialized data. Supported values are:
        - 'json'
        - 'yaml'

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of safe formats.
    """
    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Decode bytes to string for JSON/YAML parsing
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Content is not valid UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "yaml":
        try:
            import yaml  # Lazy import to avoid unnecessary dependency
        except ImportError as exc:
            raise ValueError("PyYAML is required for YAML deserialization") from exc
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ValueError("Invalid YAML data") from exc