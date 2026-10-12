import json
import configparser
from io import BytesIO
from typing import Any, Dict

__all__ = ["convert_serialized_data"]


def _parse_json(raw: bytes) -> Any:
    """
    Safely parse JSON data.

    The function explicitly decodes the bytes using UTF-8 (the standard for JSON)
    and then loads them with json.loads.  Any decoding or parsing errors are
    propagated to the caller as ValueError / JSONDecodeError.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON payload is not valid UTF-8") from exc

    return json.loads(text)


def _parse_ini(raw: bytes) -> Dict[str, Dict[str, str]]:
    """
    Safely parse INI data.

    The function reads the bytes with UTF-8 decoding and uses
    configparser.ConfigParser to parse the sections.  It returns a nested
    dictionary mapping section names to key/value pairs.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("INI payload is not valid UTF-8") from exc

    parser = configparser.ConfigParser()
    # Avoid interpolation and other features that could lead to code execution.
    parser.optionxform = str  # preserve case of keys
    try:
        parser.read_file(BytesIO(text.encode("utf-8")))
    except configparser.Error as exc:
        raise ValueError(f"Failed to parse INI data: {exc}") from exc

    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result


# Mapping of supported format hints to their parsing functions.
_SUPPORTED_FORMATS = {
    "json": _parse_json,
    "ini": _parse_ini,
}


def convert_serialized_data(raw_bytes: bytes, format_hint: str) -> Any:
    """
    Deserialize binary data using only a safe, pre‑approved format.

    Parameters
    ----------
    raw_bytes : bytes
        The binary payload to deserialize.
    format_hint : str
        A case‑insensitive hint indicating which format the payload is in.
        Supported values are ``"json"``, ``"ini"``.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    ValueError
        If the format hint is unsupported or if deserialization fails.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise ValueError("raw_bytes must be a bytes-like object")

    key = format_hint.lower()
    parser = _SUPPORTED_FORMATS.get(key)
    if parser is None:
        raise ValueError(
            f"Unsupported or unsafe format: {format_hint!r}. "
            "Allowed formats are: json, ini."
        )

    return parser(raw_bytes)