import json
import configparser
from io import BytesIO
from typing import Any


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Safely deserializes binary data from a trusted set of formats.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized data to be deserialized.
    data_format : str
        One of the supported formats: 'json' or 'ini'.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If `data_format` is not in the allowed set or if deserialization fails.
    """
    # Normalize format string
    fmt = data_format.strip().lower()

    if fmt == "json":
        try:
            # JSON is text based; decode bytes as UTF‑8
            text = byte_sequence.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON payload: {exc}") from exc

    if fmt == "ini":
        try:
            parser = configparser.ConfigParser()
            # ConfigParser expects a file‑like object
            with BytesIO(byte_sequence) as stream:
                parser.read_file(stream)
            # Convert to a plain dict for easier consumption
            return {section: dict(parser[section]) for section in parser.sections()}
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError(f"Failed to deserialize INI payload: {exc}") from exc

    # If we reach this point, the format is unsupported
    raise ValueError(f"Unsupported or unsafe deserialization format: {data_format!r}")