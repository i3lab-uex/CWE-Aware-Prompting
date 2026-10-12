import json
from configparser import ConfigParser, Error as ConfigError

class UnsupportedFormatError(ValueError):
    """Raised when the requested format is not supported for deserialization."""
    pass

class UnsafeFormatError(ValueError):
    """Raised when the requested format is known to be unsafe."""
    pass

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data into a Python object using only safe formats.

    Parameters
    ----------
    raw_bytes : bytes
        The binary data to deserialize.
    format_hint : str
        A hint of the serialization format. Supported values are:
            - 'json'   : JSON format (safe).
            - 'ini'    : INI configuration file format (safe).

    Returns
    -------
    object
        The Python representation of the deserialized data.

    Raises
    ------
    UnsupportedFormatError
        If ``format_hint`` is not one of the supported formats.
    UnsafeFormatError
        If ``format_hint`` refers to a format known to be unsafe (e.g. 'pickle').
    ValueError
        If the data cannot be parsed according to the specified format.
    """
    if not isinstance(raw_bytes, bytes):
        raise TypeError("raw_bytes must be of type 'bytes'")

    fmt = format_hint.lower()
    text = raw_bytes.decode('utf-8')

    if fmt == 'json':
        return json.loads(text)

    elif fmt == 'ini':
        parser = ConfigParser()
        try:
            parser.read_string(text)
        except ConfigError as exc:
            raise ValueError(f"Failed to parse INI data: {exc}") from exc

        # Convert the ConfigParser object into a plain dictionary.
        return {
            section: dict(parser.items(section))
            for section in parser.sections()
        }

    elif fmt == 'pickle':
        # Pickle is explicitly disallowed because it can execute arbitrary code.
        raise UnsafeFormatError("Deserialization with 'pickle' is unsafe and not permitted.")

    else:
        raise UnsupportedFormatError(f"Unsupported or unknown format: '{format_hint}'. "
                                     "Supported formats are 'json' and 'ini'.")