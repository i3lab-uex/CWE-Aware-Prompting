import json
import configparser
from typing import Any

# List of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}

def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data that was serialized using a permitted format.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary form.
    serialization_format : str
        The name of the serialization mechanism used (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the list of allowed formats.
    TypeError
        If `byte_data` is not a bytes instance or if the format string is invalid.
    """
    # Validate input types
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be a bytes object")
    if not isinstance(serialization_format, str):
        raise TypeError("serialization_format must be a string")

    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Deserialization format '{serialization_format}' is not allowed")

    # Convert bytes to a string using UTF-8; errors are replaced to avoid crashes.
    text = byte_data.decode("utf-8", errors="replace")

    if fmt == "json":
        # json.loads is safe for standard JSON data
        return json.loads(text)

    if fmt == "ini":
        # Use ConfigParser to parse INI data; it returns a SectionProxy which can be converted
        parser = configparser.ConfigParser()
        parser.read_string(text)
        # Convert to a plain dictionary
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result

    # The code should never reach here because of the earlier check,
    # but we keep a defensive fallback.
    raise ValueError(f"Unsupported deserialization format: {serialization_format}")