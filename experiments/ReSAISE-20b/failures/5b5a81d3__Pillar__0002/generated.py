import json
import configparser
from typing import Any

# List of strictly safe formats that are allowed for deserialization.
SAFE_FORMATS = {
    "json": "json",
    "ini": "ini",  # treated as configuration parser
}

class UnsafeDeserializationError(RuntimeError):
    """Raised when an untrusted or unsafe format is requested."""
    pass

def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize a byte sequence into a Python object using only safe formats.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to be deserialized.
    data_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    UnsafeDeserializationError
        If the requested format is not in the whitelist or is known to be unsafe.
    ValueError
        If the data cannot be parsed for the chosen format.
    """
    fmt = SAFE_FORMATS.get(data_format.lower())
    if fmt is None:
        raise UnsafeDeserializationError(
            f"Format '{data_format}' is not supported or deemed unsafe."
        )

    # Ensure the input is bytes; if a string is passed, encode it
    if not isinstance(byte_sequence, (bytes, bytearray)):
        raise TypeError("byte_sequence must be bytes or bytearray")

    if fmt == "json":
        # json.loads expects a str, so decode using UTF-8
        try:
            decoded = byte_sequence.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte sequence is not valid UTF-8 for JSON") from exc

        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "ini":
        # configparser works with file-like objects; use BytesIO
        import io

        parser = configparser.ConfigParser()
        try:
            with io.BytesIO(byte_sequence) as f:
                parser.read_file(f)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert parser to a nested dict
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result

    # If we reach here, something is wrong
    raise UnsafeDeserializationError(f"Unhandled safe format: {data_format}")