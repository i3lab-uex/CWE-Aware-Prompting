import json
import configparser
from typing import Any, Dict


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary data from a trusted format.

    Parameters
    ----------
    byte_sequence : bytes
        Serialized data received from an untrusted source.
    data_format : str
        The format of the serialized data. Supported formats are:
            - 'json'
            - 'ini'

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not supported or considered unsafe.
    """
    if not isinstance(byte_sequence, (bytes, bytearray)):
        raise TypeError("byte_sequence must be a bytes-like object")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            text = byte_sequence.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON payload") from exc

    if fmt == "ini":
        try:
            text = byte_sequence.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_string(text)
            # Convert ConfigParser to a plain dict
            result: Dict[str, Dict[str, str]] = {
                section: dict(parser.items(section)) for section in parser.sections()
            }
            return result
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI payload") from exc

    # Any other format is rejected to avoid unsafe deserialization
    raise ValueError(f"Unsupported or unsafe data format: {data_format}")