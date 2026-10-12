import json
import configparser
from io import BytesIO
from typing import Any


class UnsafeFormatError(ValueError):
    """Raised when an unsupported or unsafe format is requested."""


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary payloads from trusted formats only.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized data in binary form.
    data_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    UnsafeFormatError
        If the requested format is not supported or considered unsafe.
    """
    fmt = data_format.lower()

    if fmt == "json":
        try:
            text = byte_sequence.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON payload") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; BytesIO wraps the bytes
            parser.read_file(BytesIO(byte_sequence))
        except configparser.Error as exc:
            raise ValueError("Failed to parse INI payload") from exc

        # Convert the ConfigParser object into a plain dictionary
        config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
        return config_dict

    # If we reach this point, the format is unsupported
    raise UnsafeFormatError(f"Deserialization of format '{data_format}' is not allowed.")