import json
import configparser
from typing import Any, Dict

# Define a whitelist of safe formats for deserialization
_SAFE_FORMATS = {"json", "ini"}


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary payloads from trusted formats only.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to deserialize.
    data_format : str
        The format of the payload. Accepted values are 'json' and 'ini'.

    Returns
    -------
    Any
        The Python object represented by the payload.

    Raises
    ------
    ValueError
        If `data_format` is not in the whitelist of safe formats.
    json.JSONDecodeError
        If the JSON payload cannot be decoded.
    configparser.Error
        If the INI payload is malformed.
    """
    # Ensure the format is one of the safe options
    fmt = data_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unrecognized or unsafe format: {data_format!r}")

    # Convert bytes to a UTF-8 string
    try:
        payload_str = byte_sequence.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Payload must be valid UTF‑8 text") from exc

    if fmt == "json":
        # json.loads already performs validation and is safe for untrusted data
        return json.loads(payload_str)

    if fmt == "ini":
        # ConfigParser parses INI files safely. Return a nested dict.
        parser = configparser.ConfigParser()
        parser.read_string(payload_str)
        result: Dict[str, Dict[str, str]] = {
            section: dict(parser.items(section)) for section in parser.sections()
        }
        return result

    # This point should never be reached due to the whitelist check
    raise AssertionError("Unhandled format branch")