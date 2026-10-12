import json
import configparser
from io import BytesIO

class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or unsafe format is requested."""
    pass

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data safely based on a given format hint.

    Parameters
    ----------
    raw_bytes : bytes
        The binary representation of the serialized data.
    format_hint : str
        One of 'json' or 'ini'. Other values will raise an exception.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    UnsupportedFormatError
        If the format_hint is not in the safe list.
    ValueError
        If deserialization fails due to malformed data.
    """
    fmt = format_hint.lower()
    if fmt == 'json':
        try:
            text = raw_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

    if fmt == 'ini':
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object with text
            stream = BytesIO(raw_bytes)
            parser.read_file(stream)
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError(f"Failed to deserialize INI: {exc}") from exc

        # Convert the parser into a plain dict for easier consumption
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result

    # Any other format is considered unsafe or unsupported
    raise UnsupportedFormatError(f"Deserialization for format '{format_hint}' is not supported.")