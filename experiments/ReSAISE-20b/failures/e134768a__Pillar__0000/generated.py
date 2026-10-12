import json
import configparser
from typing import Any

# Define a whitelist of safe formats for deserialization.
SAFE_FORMATS = {
    "json",
    "ini",
}

def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from trusted formats only.

    Parameters
    ----------
    byte_data : bytes
        The serialized binary data.
    struct_format : str
        The format used for deserialization. Must be one of the safe formats.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested.
    json.JSONDecodeError, configparser.Error
        Propagated if the data cannot be parsed for the chosen format.
    """
    # Normalise and validate the requested format
    fmt = struct_format.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    # Convert bytes to string for text-based formats
    try:
        decoded = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if fmt == "json":
        return json.loads(decoded)

    # INI format handling
    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use read_string
        parser.read_string(decoded)
        return parser

    # This point should never be reached due to the whitelist check.
    raise ValueError(f"Unhandled format: {struct_format!r}")