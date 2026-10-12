import json
import configparser
from io import StringIO


def unpack_serialized_object(byte_data: bytes, struct_format: str):
    """
    Deserialize binary data from a trusted format.

    Parameters
    ----------
    byte_data : bytes
        The serialized binary data.
    struct_format : str
        The format of the serialized data. Supported formats are:
        - 'json'  : JSON text
        - 'ini'   : INI configuration

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    TypeError
        If ``byte_data`` is not a :class:`bytes` instance.
    ValueError
        If the format string is unknown or unsafe (e.g., 'pickle').
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be a bytes instance")

    fmt = struct_format.lower()

    if fmt == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "ini":
        try:
            text = byte_data.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(text))
            # Convert the ConfigParser to a regular dict
            result = {section: dict(parser.items(section)) for section in parser.sections()}
            return result
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError(f"Invalid INI data: {exc}") from exc

    # Reject any other format (including 'pickle', 'yaml', etc.)
    raise ValueError(f"Unsupported or unsafe serialization format: {struct_format}")