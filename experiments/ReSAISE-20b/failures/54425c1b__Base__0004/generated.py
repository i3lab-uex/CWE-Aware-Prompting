import json
import configparser
from typing import Any, Dict


# List of allowed formats for deserialization
ALLOWED_FORMATS = {"json", "ini"}


def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Deserialize binary data safely using only permitted formats.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary format.
    format_type : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS.
    json.JSONDecodeError
        If JSON data cannot be decoded.
    configparser.Error
        If INI data is malformed.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Deserialization format '{format_type}' is not allowed.")

    if fmt == "json":
        # Decode bytes to string; assume UTF-8 encoding
        text = data_input.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use BytesIO
        from io import StringIO

        # Decode bytes to string for INI parsing
        ini_text = data_input.decode("utf-8")
        parser.read_file(StringIO(ini_text))

        # Convert to a nested dictionary: {section: {key: value}}
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result