import json
import configparser
from typing import Any, Dict

class UnsupportedFormatError(RuntimeError):
    """Raised when the requested schema type is not supported or unsafe."""
    pass

def _deserialize_json(payload_bytes: bytes) -> Any:
    """
    Safely deserialize JSON data from a byte string.
    """
    try:
        text = payload_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UnsupportedFormatError("Payload is not valid UTF-8 encoded JSON") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise UnsupportedFormatError("Invalid JSON data") from exc


def _deserialize_ini(payload_bytes: bytes) -> Dict[str, Dict[str, str]]:
    """
    Safely deserialize INI data from a byte string.
    Returns a nested dictionary: {section: {option: value}}
    """
    try:
        text = payload_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UnsupportedFormatError("Payload is not valid UTF-8 encoded INI") from exc

    parser = configparser.ConfigParser()
    try:
        # read_string expects a string; no file access is performed.
        parser.read_string(text)
    except configparser.Error as exc:
        raise UnsupportedFormatError("Invalid INI data") from exc

    # Convert to a plain dictionary for easier consumption.
    return {section: dict(parser.items(section)) for section in parser.sections()}


def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Deserialize binary data according to a safe, pre‑approved schema type.

    Parameters
    ----------
    payload_bytes : bytes
        The raw binary payload to deserialize.
    schema_type : str
        One of the supported schema types: 'json' or 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    UnsupportedFormatError
        If the schema_type is not supported or if deserialization fails.
    """
    # Normalise the schema type to avoid case‑sensitivity issues
    fmt = schema_type.strip().lower()

    if fmt == "json":
        return _deserialize_json(payload_bytes)
    elif fmt == "ini":
        return _deserialize_ini(payload_bytes)

    # If we reach this point the format is not in our curated list
    raise UnsupportedFormatError(f"Unsupported or unsafe schema type: {schema_type!r}")