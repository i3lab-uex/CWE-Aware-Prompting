import json
import configparser
from typing import Any, Dict


def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary format.
    format_type : str
        Serialization mechanism used ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict for JSON or ini).

    Raises
    ------
    ValueError
        If the format_type is not supported or if deserialization fails.
    """
    if not isinstance(data_input, bytes):
        raise ValueError("data_input must be of type 'bytes'")

    fmt = format_type.lower()

    try:
        if fmt == "json":
            # Decode bytes to string using UTF-8 and parse JSON
            text = data_input.decode("utf-8")
            return json.loads(text)

        elif fmt == "ini":
            # Decode bytes to string and parse INI into a nested dict
            text = data_input.decode("utf-8")
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(text)
            result: Dict[str, Dict[str, str]] = {}
            for section in parser.sections():
                result[section] = dict(parser.items(section))
            return result

        else:
            raise ValueError(f"Unsupported format_type: {format_type!r}")

    except (UnicodeDecodeError, json.JSONDecodeError, configparser.Error) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc