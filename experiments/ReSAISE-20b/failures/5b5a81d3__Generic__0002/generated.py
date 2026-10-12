import json
import configparser
from typing import Any, Dict

__all__ = ["deserialize_payload"]

# Only these formats are considered safe for deserialization
ALLOWED_FORMATS = {"json", "ini"}


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize a binary payload into a Python object using only safe, predefined formats.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to deserialize.
    data_format : str
        The format used for deserialization. Supported values are:
            * "json" – JSON data.
            * "ini"  – INI configuration files.

    Returns
    -------
    Any
        The deserialized Python object. For JSON this is the native Python representation.
        For INI this function returns a dictionary of dictionaries
        (``{section: {key: value, ...}, ...}``).

    Raises
    ------
    ValueError
        If `data_format` is not one of the allowed formats.
    UnicodeDecodeError
        If the byte sequence cannot be decoded as UTF‑8 (JSON and INI are text based).
    json.JSONDecodeError
        If the JSON payload is malformed.
    configparser.Error
        If the INI payload cannot be parsed.

    Notes
    -----
    * Pickle, marshal and other binary formats are deliberately excluded because they can execute arbitrary code.
    * The function does not perform any schema validation; callers should validate the resulting data as needed.
    """
    if data_format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format '{data_format}'. Allowed formats: {sorted(ALLOWED_FORMATS)}")

    # Decode bytes to string – both JSON and INI are text formats.
    try:
        text = byte_sequence.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            "UTF‑8 decoding failed",
            byte_sequence,
            exc.startchar,
            exc.endchar,
            f"Could not decode payload as UTF‑8 for format '{data_format}'.",
        ) from exc

    if data_format == "json":
        return json.loads(text)

    # data_format == "ini"
    parser = configparser.ConfigParser()
    parser.read_string(text)
    result: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result