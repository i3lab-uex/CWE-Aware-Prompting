import json
import configparser
from typing import Any, Dict

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}

def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using only a whitelist of safe formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        The format of the serialized data (e.g. 'json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not recognized or deemed unsafe.
    TypeError
        If `byte_data` is not of type `bytes`.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    fmt = struct_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    # Decode bytes to text using UTF-8.  Errors are ignored to avoid crashes on malformed data.
    text = byte_data.decode("utf-8", errors="ignore")

    if fmt == "json":
        return json.loads(text)

    # For ini format, parse into a nested dictionary.
    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser requires a file-like object; use `read_string`.
        parser.read_string(text)
        # Convert to a regular dict for easier consumption.
        result: Dict[str, Dict[str, str]] = {
            section: dict(parser.items(section)) for section in parser.sections()
        }
        return result

    # This point should never be reached due to the whitelist check.
    raise ValueError(f"Unhandled format: {struct_format!r}")