import json
import configparser
from io import BytesIO
from typing import Any

# List of allowed serialization formats
ALLOWED_FORMATS = {"json", "ini"}

class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or disallowed format is requested."""
    pass

def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Safely deserialize binary data that was serialized using a permitted format.

    Parameters
    ----------
    data_input : bytes
        Serialized binary data received from an external source.
    format_type : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not in ALLOWED_FORMATS.
    ValueError
        If deserialization fails due to malformed input.
    """
    if format_type not in ALLOWED_FORMATS:
        raise UnsupportedFormatError(
            f"Deserialization for format '{format_type}' is not allowed."
        )

    try:
        if format_type == "json":
            # JSON expects a string; decode bytes safely
            decoded = data_input.decode("utf-8")
            return json.loads(decoded)

        elif format_type == "ini":
            # INI files are parsed into a ConfigParser object
            parser = configparser.ConfigParser()
            # Use BytesIO to read bytes directly
            with BytesIO(data_input) as stream:
                parser.read_file(stream)
            # Convert to a nested dictionary for easier consumption
            ini_dict = {
                section: dict(parser.items(section))
                for section in parser.sections()
            }
            return ini_dict

    except Exception as exc:
        # Wrap any exception to provide context without exposing raw trace
        raise ValueError(f"Failed to deserialize data: {exc}") from exc