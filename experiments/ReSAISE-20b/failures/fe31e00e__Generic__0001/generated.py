import json
import configparser
from typing import Any

def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary format.
    serialization_format : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    Any
        Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or not allowed.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {
        'json',
        'ini',   # INI is parsed into a ConfigParser object
    }

    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {serialization_format!r}")

    if fmt == 'json':
        # json.loads expects a str; decode using utf-8
        try:
            return json.loads(byte_data.decode('utf-8'))
        except UnicodeDecodeError as exc:
            raise ValueError("Byte data is not valid UTF-8 for JSON.") from exc
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if fmt == 'ini':
        parser = configparser.ConfigParser()
        try:
            # ConfigParser.read_string expects a string; decode using utf-8
            parser.read_string(byte_data.decode('utf-8'))
        except UnicodeDecodeError as exc:
            raise ValueError("Byte data is not valid UTF-8 for INI.") from exc
        except configparser.Error as exc:
            raise ValueError("Invalid INI data.") from exc
        # Convert ConfigParser to a nested dict for easier use
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result

    # Should never reach here due to whitelist, but keep for completeness
    raise ValueError(f"Unhandled format: {serialization_format!r}")