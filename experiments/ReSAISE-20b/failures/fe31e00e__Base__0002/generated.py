import json
import configparser
from typing import Any


class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or unsafe serialization format is requested."""


class DeserializationError(RuntimeError):
    """Raised when deserialization fails for any reason."""


def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary form.
    serialization_format : str
        The name of the serialization format. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    UnsupportedFormatError
        If the requested format is not on the safe list.
    DeserializationError
        If deserialization fails for any reason (e.g., malformed data).
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    fmt = serialization_format.lower()
    data_str = byte_data.decode("utf-8")  # Decode assuming UTF‑8; adjust if needed

    try:
        if fmt == "json":
            return json.loads(data_str)

        elif fmt == "ini":
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(data_str)
            # Convert to a nested dictionary for easier consumption
            return {section: dict(parser.items(section)) for section in parser.sections()}

        else:
            raise UnsupportedFormatError(
                f"Deserialization format '{serialization_format}' is not supported or unsafe."
            )

    except Exception as exc:
        # Wrap any exception that occurs during parsing
        raise DeserializationError(
            f"Failed to deserialize data using format '{serialization_format}': {exc}"
        ) from exc