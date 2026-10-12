import json
from typing import Any

# Import PyYAML only if available; otherwise fall back to a minimal safe subset.
try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# List of formats considered safe for deserialization.
ALLOWED_FORMATS = {
    "json",
    "yaml",   # Requires PyYAML's safe_load
}

def _decode_json(data: bytes) -> Any:
    """Deserialize JSON data."""
    text = data.decode("utf-8")
    return json.loads(text)

def _decode_yaml(data: bytes) -> Any:
    """Deserialize YAML data using safe_load."""
    if yaml is None:  # pragma: no cover
        raise RuntimeError("PyYAML is required for YAML deserialization.")
    text = data.decode("utf-8")
    return yaml.safe_load(text)

# Mapping from format name to decoding function.
DECODERS = {
    "json": _decode_json,
    "yaml": _decode_yaml,
}

def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    data : bytes
        Serialized byte stream.
    data_format : str
        Format of the serialized data ('json', 'yaml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the allowed list.
    RuntimeError
        If a required dependency (e.g., PyYAML) is missing for the chosen format.
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be of type 'bytes'")

    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    decoder = DECODERS[fmt]
    return decoder(data)