import json
import configparser
from typing import Any


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Safely deserializes binary data from a trusted set of formats.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to be deserialized.
    data_format : str
        The format of the serialized data. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or if decoding fails.
    """
    # Normalize format string
    fmt = data_format.lower().strip()

    try:
        decoded_text = byte_sequence.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte sequence is not valid UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(decoded_text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(decoded_text)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert to a plain dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    raise ValueError(f"Unsupported or unsafe format: {data_format}")