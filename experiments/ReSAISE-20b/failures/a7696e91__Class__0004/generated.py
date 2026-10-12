import json
from configparser import ConfigParser, NoSectionError, NoOptionError
from typing import Any

# Whitelist of safe serialization formats
SAFE_FORMATS = {"json", "ini"}

def _deserialize_json(data: bytes) -> Any:
    """Deserialize JSON data."""
    text = data.decode("utf-8")
    return json.loads(text)

def _deserialize_ini(data: bytes) -> dict:
    """Deserialize INI data into a nested dictionary."""
    text = data.decode("utf-8")
    parser = ConfigParser()
    parser.read_string(text)

    result: dict[str, dict[str, str]] = {}
    for section in parser.sections():
        result[section] = {}
        for key, value in parser.items(section):
            result[section][key] = value
    return result

DESERIALIZE_MAP = {
    "json": _deserialize_json,
    "ini":  _deserialize_ini,
}

def load_serialized_content(serialized_input: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize binary data from trusted formats.

    Parameters
    ----------
    serialized_input : bytes
        Binary representation of the serialized data.
    serialization_format : str
        Identifier of the serialization format (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    deserializer = DESERIALIZE_MAP[fmt]
    return deserializer(serialized_input)