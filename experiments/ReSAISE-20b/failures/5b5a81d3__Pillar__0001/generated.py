import json
import configparser
from io import BytesIO
from typing import Any


# Define the set of safe formats that are allowed.
SAFE_FORMATS = {"json", "ini"}


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using only safe formats.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized data in binary form.
    data_format : str
        The format used for deserialization. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the data_format is not recognized or considered unsafe.
    json.JSONDecodeError, configparser.Error
        If the data cannot be parsed for the given format.
    """
    fmt = data_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    if fmt == "json":
        # Assume UTF-8 encoding for JSON payloads.
        try:
            text = byte_sequence.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON payload is not valid UTF-8") from exc
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            with BytesIO(byte_sequence) as stream:
                parser.read_file(stream)
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Failed to parse INI payload") from exc
        # Convert ConfigParser data into a plain dictionary.
        return {section: dict(parser[section]) for section in parser.sections()}