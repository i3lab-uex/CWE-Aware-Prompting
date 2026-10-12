import json
import configparser
from io import StringIO

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Safely deserialize binary data using a restricted set of formats.

    Supported formats:
        - 'json' : JSON encoded data
        - 'ini'  : INI configuration files

    Parameters:
        data_input (bytes): Binary payload received from an external source.
        format_type (str): Identifier of the serialization mechanism.

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the format is unsupported or disallowed.
        json.JSONDecodeError: If JSON parsing fails.
        configparser.Error: If INI parsing fails.
    """
    if not isinstance(data_input, bytes):
        raise TypeError("data_input must be of type 'bytes'")

    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json", "ini"}

    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Deserialization format '{format_type}' is not allowed")

    # Convert bytes to string for parsing
    try:
        text = data_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8 encoded text") from exc

    if fmt == "json":
        # json.loads is safe for standard data types
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # Use read_string which expects a string; errors will raise
        parser.read_string(text)
        # Convert to a plain dictionary for easier consumption
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Should never reach here because of the whitelist check
    raise ValueError(f"Unhandled format: {format_type}")