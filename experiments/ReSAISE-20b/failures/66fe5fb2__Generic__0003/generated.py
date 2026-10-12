import json
import configparser
from typing import Any


class UnsupportedFormatError(ValueError):
    """Raised when the provided format is not allowed for deserialization."""


class DeserializationError(Exception):
    """Raised when the data cannot be deserialized successfully."""


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        Serialized data received in binary format.
    method_format : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    Any
        Python object resulting from deserialization.

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not allowed.
    DeserializationError
        If deserialization fails for any reason.
    """
    if not isinstance(serialized_bytes, bytes):
        raise TypeError("serialized_bytes must be a bytes object")

    fmt = method_format.lower()

    try:
        if fmt == "json":
            # Decode bytes to string and parse JSON
            text = serialized_bytes.decode("utf-8")
            return json.loads(text)

        elif fmt == "ini":
            # Parse INI data into a dictionary
            parser = configparser.ConfigParser()
            parser.read_string(serialized_bytes.decode("utf-8"))
            # Convert to a nested dictionary
            result = {section: dict(parser.items(section)) for section in parser.sections()}
            return result

        else:
            raise UnsupportedFormatError(f"Deserialization format '{method_format}' is not supported or allowed.")
    except Exception as exc:
        # Wrap any exception into DeserializationError for clarity
        raise DeserializationError(f"Failed to deserialize data: {exc}") from exc