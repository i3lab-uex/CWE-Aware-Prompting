import json
import configparser
from typing import Any, Dict

# Whitelisted formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data based on a trusted format identifier.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format (e.g. 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    TypeError
        If ``data_bytes`` is not a bytes instance.
    ValueError
        If the format string is not in the allowed list or if deserialization fails.
    """
    if not isinstance(data_bytes, bytes):
        raise TypeError("data_bytes must be a bytes object")

    fmt = format_string.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string}")

    # Decode bytes to string using UTF-8; errors='strict' ensures we fail on bad data.
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use read_string.
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the parser to a dictionary for easier consumption.
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point should never be reached because of the earlier whitelist check.
    raise ValueError(f"Unhandled format: {format_string}")