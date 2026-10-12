import json
import configparser
from io import StringIO

class UnsupportedSerializationFormatError(RuntimeError):
    """Raised when an unsupported or unsafe serialization format is requested."""
    pass

def load_serialized_content(serialized_input: bytes, serialization_format: str):
    """
    Deserialize binary data from a trusted format.

    Parameters
    ----------
    serialized_input : bytes
        The input data in binary form.
    serialization_format : str
        The format of the serialized data. Only 'json' and 'ini' are supported.

    Returns
    -------
    Any
        The deserialized Python object. For JSON this is a dict/list; for INI
        this is a nested dictionary: {section: {key: value}}.

    Raises
    ------
    UnsupportedSerializationFormatError
        If the format is not recognized or considered unsafe.
    ValueError
        If the data cannot be parsed in the given format.
    """
    if not isinstance(serialized_input, (bytes, bytearray)):
        raise TypeError("serialized_input must be bytes or bytearray")

    fmt = serialization_format.lower()
    try:
        text = serialized_input.decode('utf-8')
    except Exception as exc:  # pragma: no cover
        raise ValueError("Input data must be UTF‑8 encoded text") from exc

    if fmt == 'json':
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:  # pragma: no cover
            raise ValueError("Invalid JSON data") from exc

    if fmt == 'ini':
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            with StringIO(text) as f:
                parser.read_file(f)
        except configparser.Error as exc:  # pragma: no cover
            raise ValueError("Invalid INI data") from exc

        # Convert to a plain dict of dicts
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # All other formats are considered unsafe or unsupported
    raise UnsupportedSerializationFormatError(
        f"Unsupported serialization format: {serialization_format!r}"
    )