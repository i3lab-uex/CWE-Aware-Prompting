import json
import configparser
from typing import Any, Dict


# Define the list of trusted formats
_TRUSTED_FORMATS = {"json", "ini"}


def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize data from a trusted source.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary format.
    format_string : str
        Identifier of the serialization format. Must be one of the trusted formats.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or untrusted.
    """
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be a bytes-like object")

    fmt = format_string.lower()
    if fmt not in _TRUSTED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_string}")

    # Decode bytes to string using UTF-8
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if fmt == "json":
        # json.loads is safe for JSON data; it will raise ValueError on malformed input
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use read_string
        parser.read_string(text)
        # Convert the ConfigParser into a nested dictionary
        result: Dict[str, Dict[str, str]] = {
            section: dict(parser.items(section)) for section in parser.sections()
        }
        return result

    # The check above ensures we never reach this point, but keep for completeness
    raise ValueError(f"Unhandled format: {format_string}")