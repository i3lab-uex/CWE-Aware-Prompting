import json
import configparser
from io import BytesIO


def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Safely deserialize binary data from a limited set of supported formats.

    Parameters
    ----------
    bin_data : bytes
        The serialized data in binary form.
    format_type : str
        One of 'json' or 'ini'. Any other value raises an exception.

    Returns
    -------
    object
        The deserialized Python object. For 'json' this is a native
        Python data structure (dict, list, etc.). For 'ini' it returns
        a :class:`configparser.ConfigParser` instance.

    Raises
    ------
    ValueError
        If the format_type is not supported or deemed unsafe.
    """
    if not isinstance(bin_data, bytes):
        raise TypeError("bin_data must be of type 'bytes'")

    fmt = format_type.lower()
    if fmt == "json":
        try:
            return json.loads(bin_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; BytesIO provides that
            parser.read_file(BytesIO(bin_data))
        except configparser.Error as exc:
            raise ValueError(f"Invalid INI data: {exc}") from exc
        return parser

    # All other formats are considered unsafe or unsupported
    raise ValueError(f"Unsupported or unsafe format_type: '{format_type}'")