import json
import configparser
from typing import Any, Dict

def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data using only a controlled set of safe formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data received in binary format.
    serialization_format : str
        The name of the serialization mechanism used
        ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or not allowed.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        try:
            text = byte_data.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_string(text)
            # Convert to a plain dictionary for easier use
            return {section: dict(parser[section]) for section in parser.sections()}
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI data") from exc

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Deserialization for format '{serialization_format}' is not allowed.")