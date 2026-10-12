import json
import configparser
from typing import Any

def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize binary data that was serialized using a controlled list of formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data in binary form.
    serialization_format : str
        One of the supported formats: 'json' or 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or deserialization fails.
    """
    if not isinstance(byte_data, bytes):
        raise ValueError("byte_data must be of type 'bytes'")

    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            # json.loads expects a string, so decode using UTF-8
            return json.loads(byte_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON data: {exc}") from exc

    elif fmt == "ini":
        try:
            parser = configparser.ConfigParser()
            # read_string expects a string, decode bytes
            parser.read_string(byte_data.decode("utf-8"))
            # Convert ConfigParser object to a plain dict
            result = {section: dict(parser.items(section)) for section in parser.sections()}
            return result
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError(f"Failed to parse INI data: {exc}") from exc

    else:
        raise ValueError(f"Unsupported or disallowed serialization format: '{serialization_format}'")