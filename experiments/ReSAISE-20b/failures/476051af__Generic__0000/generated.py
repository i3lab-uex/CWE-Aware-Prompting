import json
import configparser
from io import BytesIO
from typing import Any


def deserialize_binary_data(bin_data: bytes, format_type: str) -> Any:
    """
    Deserialize binary data into a Python object using only safe formats.

    Supported formats (case‑insensitive):
        - 'json' : JSON data
        - 'ini'  : INI configuration files

    Parameters
    ----------
    bin_data : bytes
        The binary payload to deserialize.
    format_type : str
        The format of the data. Must be one of the supported formats.

    Returns
    -------
    Any
        The Python representation of the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not supported or if deserialization fails.
    """
    if not isinstance(bin_data, (bytes, bytearray)):
        raise ValueError("bin_data must be bytes or bytearray")

    fmt = format_type.strip().lower()
    if fmt == "json":
        try:
            # json.loads expects a string, so decode using utf-8
            return json.loads(bin_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if fmt == "ini":
        try:
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object, use BytesIO
            with BytesIO(bin_data) as f:
                parser.read_file(f)
            # Convert the ConfigParser to a nested dict
            return {section: dict(parser.items(section)) for section in parser.sections()}
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Failed to deserialize INI data") from exc

    # If we reach here, the format is unsupported
    raise ValueError(f"Unsupported or unsafe format: {format_type!r}")