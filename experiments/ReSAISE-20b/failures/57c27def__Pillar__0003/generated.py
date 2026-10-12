import json
import configparser
from io import StringIO

class UnsupportedFormatError(RuntimeError):
    """Raised when the requested format is not supported or considered unsafe."""
    pass

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data safely based on a limited set of supported formats.

    Parameters
    ----------
    raw_bytes : bytes
        The serialized data in binary form.
    format_hint : str
        A hint indicating which format to use for deserialization. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    object
        The Python representation of the deserialized data.

    Raises
    ------
    UnsupportedFormatError
        If the format_hint is not supported or considered unsafe.
    ValueError
        If deserialization fails due to malformed data.
    """
    fmt = format_hint.lower()

    if fmt == "json":
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF-8 encoded") from exc
        return json.loads(text)

    if fmt == "ini":
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("INI data must be UTF-8 encoded") from exc
        parser = configparser.ConfigParser()
        # Using StringIO ensures the file-like object is properly closed
        with StringIO(text) as f:
            parser.read_file(f)
        # Convert to a plain dict for easier consumption
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # All other formats are considered unsafe or unsupported
    raise UnsupportedFormatError(f"Deserialization for format '{format_hint}' is not supported or unsafe.")