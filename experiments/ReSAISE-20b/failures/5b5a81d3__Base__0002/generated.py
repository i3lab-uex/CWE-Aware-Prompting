import json
import configparser
from typing import Any, Union

# Define the set of safe formats that are allowed for deserialization.
SAFE_FORMATS = {"json", "ini"}

class UnsupportedFormatError(ValueError):
    """Raised when an unsupported or unsafe format is requested."""
    pass

def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize a binary payload into a Python object using only safe formats.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to deserialize.
    data_format : str
        The name of the format used for deserialization. Must be one of the
        values in `SAFE_FORMATS`.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    UnsupportedFormatError
        If `data_format` is not in the list of safe formats.
    ValueError
        If deserialization fails due to malformed data.
    """
    # Normalise the format string for comparison
    fmt = data_format.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise UnsupportedFormatError(
            f"Deserialization format '{data_format}' is not supported or unsafe."
        )

    try:
        # Decode the byte sequence to a string (UTF‑8 is the common default).
        text = byte_sequence.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded as UTF‑8.") from exc

    if fmt == "json":
        # json.loads safely converts JSON into Python objects.
        return json.loads(text)

    if fmt == "ini":
        # ConfigParser safely parses INI files into a ConfigParser instance.
        parser = configparser.ConfigParser()
        # read_string expects a string with newline separators.
        parser.read_string(text)
        return parser

    # The code should never reach this point because all supported formats
    # are handled above.  This is a defensive guard.
    raise UnsupportedFormatError(f"Unhandled format '{data_format}'.")