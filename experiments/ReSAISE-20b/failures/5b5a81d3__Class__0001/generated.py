import json
import configparser
from typing import Any, Dict

def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary payloads from untrusted sources while restricting
    the operation to a small set of safe formats.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized data in binary form.
    data_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not recognized or deemed unsafe.
    UnicodeDecodeError
        If the byte sequence cannot be decoded as UTF‑8 (required for all supported formats).
    """
    # Normalize the format string
    fmt = data_format.strip().lower()

    if fmt not in {"json", "ini"}:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    # All supported formats operate on UTF‑8 text
    try:
        decoded = byte_sequence.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte sequence is not valid UTF‑8") from exc

    if fmt == "json":
        # json.loads is safe for trusted data; it does not execute code.
        return json.loads(decoded)

    if fmt == "ini":
        # Parse INI data into a nested dictionary
        parser = configparser.ConfigParser()
        parser.read_string(decoded)
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point is unreachable due to the earlier check, but keep for completeness
    raise ValueError(f"Unhandled format: {data_format!r}")