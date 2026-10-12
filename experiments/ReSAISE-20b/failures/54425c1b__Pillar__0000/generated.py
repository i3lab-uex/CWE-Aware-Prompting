import json
import configparser
from io import StringIO

class UnsupportedFormatError(ValueError):
    """Raised when an unsupported or disallowed format is requested."""
    pass

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Safely deserializes binary data according to a whitelist of formats.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary format.
    format_type : str
        The serialization mechanism used ('json' or 'ini').

    Returns
    -------
    Any
        The deserialized Python object (dict, list, etc.).

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not in the whitelist.
    """
    if not isinstance(data_input, bytes):
        raise TypeError("data_input must be of type 'bytes'")

    fmt = format_type.lower()
    # Whitelist of safe formats
    if fmt == 'json':
        try:
            text = data_input.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

    if fmt == 'ini':
        try:
            text = data_input.decode('utf-8')
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(text))
            # Convert ConfigParser to a plain dict
            return {section: dict(parser[section]) for section in parser.sections()}
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError(f"Failed to deserialize INI: {exc}") from exc

    # Any other format is disallowed
    raise UnsupportedFormatError(
        f"Deserialization for format '{format_type}' is not supported or allowed."
    )