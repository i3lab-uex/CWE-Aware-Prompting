import json
import configparser
from typing import Any, Dict

def convert_serialized_data(raw_bytes: bytes, format_hint: str) -> Any:
    """
    Deserialize binary data safely based on a provided format hint.

    Supported formats (safe):
        - 'json' : JSON encoded data.
        - 'ini'  : INI style configuration data.

    Parameters
    ----------
    raw_bytes : bytes
        Binary payload containing the serialized representation.
    format_hint : str
        The expected serialization format (case-insensitive).

    Returns
    -------
    Any
        The deserialized Python object. For JSON it returns the native
        representation; for INI it returns a nested dictionary of sections.

    Raises
    ------
    ValueError
        If the format_hint is unsupported or the data cannot be parsed.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise ValueError("raw_bytes must be a bytes-like object")

    fmt = format_hint.lower()
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Unable to decode bytes as UTF-8: {exc}") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON deserialization failed: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError(f"INI parsing failed: {exc}") from exc

        # Convert the ConfigParser object into a plain dictionary
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported or unsafe format: '{format_hint}'")