import json
from configparser import ConfigParser
from typing import Any


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary payloads from untrusted sources.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to deserialize.
    data_format : str
        One of the supported safe formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or considered unsafe.
    """
    # Normalize format string for case‑insensitivity
    fmt = data_format.strip().lower()

    if fmt == "json":
        try:
            text = byte_sequence.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if fmt == "ini":
        try:
            text = byte_sequence.decode("utf-8")
            parser = ConfigParser()
            # read_string expects a string with at least one section header
            parser.read_string(text)
            return {
                section: dict(parser.items(section))
                for section in parser.sections()
            }
        except (UnicodeDecodeError, ValueError) as exc:
            raise ValueError(f"Invalid INI payload: {exc}") from exc

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported or unsafe deserialization format: '{data_format}'")