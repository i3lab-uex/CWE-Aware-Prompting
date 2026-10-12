import json
import configparser
from io import BytesIO

class UnsupportedFormatError(ValueError):
    """Raised when the requested format is not supported or considered unsafe."""
    pass

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data safely based on the provided format hint.

    Supported formats:
        - 'json': JSON text encoded in UTF-8.
        - 'ini' : INI configuration data.

    Parameters
    ----------
    raw_bytes : bytes
        The binary representation of the serialized data.
    format_hint : str
        A string indicating which deserialization routine to use.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    UnsupportedFormatError
        If the format_hint is not supported or considered unsafe.
    """
    fmt = format_hint.lower()

    if fmt == 'json':
        try:
            return json.loads(raw_bytes.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise UnsupportedFormatError(f"Invalid JSON data: {exc}") from exc

    if fmt == 'ini':
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; BytesIO provides that.
            parser.read_file(BytesIO(raw_bytes))
        except configparser.Error as exc:
            raise UnsupportedFormatError(f"Invalid INI data: {exc}") from exc

        # Convert ConfigParser object to a nested dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # All other formats are either unsupported or unsafe (e.g., pickle)
    raise UnsupportedFormatError(f"Unsupported or unsafe format: {format_hint}")