import json
import configparser
from typing import Any

def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize binary data using only approved formats.

    Args:
        byte_data: Serialized data in bytes.
        serialization_format: One of the supported formats
            ('json', 'ini').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the format is not supported or data cannot be parsed.
    """
    # Normalize format string
    fmt = serialization_format.strip().lower()

    if fmt == "json":
        try:
            # JSON must be text; decode using UTF-8
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        # ConfigParser expects a file-like object; use read_string
        parser = configparser.ConfigParser()
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("INI data is not valid UTF-8") from exc
        try:
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc
        # Convert parser to a nested dict for easier consumption
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result

    # If we reach here, the format is not supported
    raise ValueError(f"Unsupported serialization format: {serialization_format}")