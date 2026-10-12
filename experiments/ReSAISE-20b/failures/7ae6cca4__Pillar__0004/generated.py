import json
import configparser
from typing import Any

# Define the list of trusted, safe formats.
ALLOWED_FORMATS = {"json", "ini"}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data according to a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or untrusted.
    json.JSONDecodeError, configparser.Error
        Propagated if the data cannot be parsed in the chosen format.
    """
    fmt = format_string.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Decode the bytes to a string using UTF-8; errors are replaced to avoid crashes.
    text = data_bytes.decode("utf-8", errors="replace")

    if fmt == "json":
        # json.loads is safe for trusted input; no code execution.
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # read_string expects a string with INI content.
        parser.read_string(text)
        # Convert to a nested dictionary for easier consumption.
        return {section: dict(parser[section]) for section in parser.sections()}

    # The following line is unreachable due to the earlier check,
    # but keeps type-checkers happy.
    raise ValueError(f"Unhandled format: {format_string!r}")