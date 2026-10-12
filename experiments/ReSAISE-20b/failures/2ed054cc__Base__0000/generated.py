import json
from typing import Any

# Optional: yaml support if PyYAML is available
try:
    import yaml
    _yaml_available = True
except ImportError:  # pragma: no cover
    _yaml_available = False

def _deserialize_json(raw_data: bytes) -> Any:
    """Deserialize JSON data."""
    text = raw_data.decode("utf-8")
    return json.loads(text)

def _deserialize_yaml(raw_data: bytes) -> Any:
    """Deserialize YAML data using safe_load."""
    if not _yaml_available:  # pragma: no cover
        raise ValueError("YAML deserialization requested but PyYAML is not installed.")
    text = raw_data.decode("utf-8")
    return yaml.safe_load(text)

# Mapping of allowed formats to their deserialization functions
_ALLOWED_FORMATS = {
    "json": _deserialize_json,
    # Only enable yaml if the library is available
    **({"yaml": _deserialize_yaml} if _yaml_available else {}),
}

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize `raw_data` using a restricted set of formats.

    Parameters
    ----------
    raw_data : bytes
        The serialized representation of the data.
    serialization_format : str
        The format used for serialization. Supported values are 'json' and, if available,
        'yaml'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported serialization format '{serialization_format}'. "
            "Allowed formats: " + ", ".join(_ALLOWED_FORMATS.keys())
        )

    try:
        return _ALLOWED_FORMATS[fmt](raw_data)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to deserialize data using format '{serialization_format}': {exc}") from exc