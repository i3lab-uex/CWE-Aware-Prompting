import json
import configparser
from typing import Any

# Define the set of formats that are considered safe.
SAFE_FORMATS = {"json", "ini"}

class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or unsafe format is requested."""
    pass

def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using only a
    predefined safe set of formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        One of the supported formats: 'json' or 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not in SAFE_FORMATS.
    ValueError
        If the data cannot be parsed for the chosen format.
    """
    # Normalise and validate the requested format
    fmt = struct_format.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise UnsupportedFormatError(
            f"Unsupported or unsafe format '{struct_format}'. "
            f"Allowed formats: {', '.join(SAFE_FORMATS)}."
        )

    # Decode bytes to a string.  UTF‑8 is used for all formats.
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8 encoded text.") from exc

    # Deserialize according to the chosen format
    if fmt == "json":
        return json.loads(text)

    # ini: parse into a ConfigParser object, then convert to a nested dict
    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data.") from exc

        # Convert to a plain dictionary for easier consumption
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result

    # This point should never be reached because of the earlier check
    raise UnsupportedFormatError(f"Unhandled format '{fmt}'.")