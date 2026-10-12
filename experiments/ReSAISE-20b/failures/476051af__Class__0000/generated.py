import json
import configparser
from typing import Any, Dict

def deserialize_binary_data(bin_data: bytes, format_type: str) -> Any:
    """
    Deserialize binary data safely for a limited set of formats.

    Parameters
    ----------
    bin_data : bytes
        Serialized data in binary form.
    format_type : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe, or if decoding fails.
    """
    # Ensure we have a string representation of the data
    try:
        text = bin_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data could not be decoded using UTF-8") from exc

    fmt = format_type.lower()

    if fmt == 'json':
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == 'ini':
        parser = configparser.ConfigParser()
        try:
            # configparser expects a file-like object; use read_string
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the ConfigParser object into a plain dict
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    else:
        # Unsupported or unsafe format
        raise ValueError(f"Unsupported or unsafe deserialization format: {format_type}")