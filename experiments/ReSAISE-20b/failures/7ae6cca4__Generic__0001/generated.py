import json
import configparser
from typing import Any

# Define the set of trusted formats
TRUSTED_FORMATS = {"json", "ini"}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize data from a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format ('json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or untrusted.
    """
    fmt = format_string.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Decode bytes to string using UTF-8 (common for text formats)
    try:
        decoded = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if fmt == "json":
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; read_string works with a string
            parser.read_string(decoded)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc
        # Convert to a plain dict: {section: {option: value}}
        return {
            section: dict(parser.items(section))
            for section in parser.sections()
        }

    # Should never reach here due to earlier check
    raise ValueError(f"Unhandled format: {format_string!r}")