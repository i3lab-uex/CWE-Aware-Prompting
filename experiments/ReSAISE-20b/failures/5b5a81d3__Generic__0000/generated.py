import json
import configparser
from typing import Any, Union

def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary data from a trusted source using only safe, predefined formats.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to deserialize.
    data_format : str
        One of the accepted format identifiers: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    if not isinstance(byte_sequence, bytes):
        raise TypeError("byte_sequence must be of type 'bytes'")

    fmt = data_format.lower()

    if fmt == "json":
        try:
            # Decode as UTF-8 before parsing
            text = byte_sequence.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        try:
            text = byte_sequence.decode("utf-8")
            parser = configparser.ConfigParser()
            # ConfigParser requires a file-like object
            from io import StringIO

            parser.read_file(StringIO(text))
            # Convert to a nested dict for easier consumption
            config_dict = {
                section: dict(parser.items(section))
                for section in parser.sections()
            }
            return config_dict
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI data") from exc

    # Add more safe formats here if needed (e.g., 'xml' with a secure parser)

    raise ValueError(f"Unsupported or unsafe data format: {data_format}")