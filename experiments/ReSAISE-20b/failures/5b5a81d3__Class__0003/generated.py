import json
import configparser
from typing import Any, Dict


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Safely deserialize binary payloads from trusted formats only.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized data.
    data_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object represented by the payload.

    Raises
    ------
    ValueError
        If the requested format is unsupported or if deserialization fails.
    """
    # Normalise format string
    fmt = data_format.strip().lower()

    if fmt == "json":
        try:
            text = byte_sequence.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON payload") from exc

    if fmt == "ini":
        try:
            text = byte_sequence.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_string(text)
            # Convert to a plain dict for easier use
            result: Dict[str, Dict[str, str]] = {
                section: dict(parser[section]) for section in parser.sections()
            }
            return result
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Failed to deserialize INI payload") from exc

    # Unsupported format
    raise ValueError(f"Unsupported or unsafe deserialization format: {data_format}")