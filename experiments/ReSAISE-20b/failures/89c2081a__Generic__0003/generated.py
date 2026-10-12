import json
import configparser
from typing import Any, Dict

class UnsupportedFormatError(ValueError):
    """Raised when the provided schema_type is not supported or considered unsafe."""
    pass

def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Safely deserialize binary payloads using a curated list of formats.

    Parameters
    ----------
    payload_bytes : bytes
        The binary data to deserialize.
    schema_type : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not in the curated list.
    ValueError
        If deserialization fails due to malformed data.
    """
    if not isinstance(payload_bytes, bytes):
        raise TypeError("payload_bytes must be of type 'bytes'")

    fmt = schema_type.lower()
    if fmt == "json":
        try:
            text = payload_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON payload") from exc

    if fmt == "ini":
        try:
            text = payload_bytes.decode("utf-8")
            parser = configparser.ConfigParser()
            # Use read_string to parse from a string instead of file
            parser.read_string(text)
            result: Dict[str, Dict[str, str]] = {
                section: dict(parser.items(section)) for section in parser.sections()
            }
            return result
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI payload") from exc

    # If the format is not in the curated safe list, raise an error
    raise UnsupportedFormatError(f"Unsupported or unsafe format: {schema_type}")