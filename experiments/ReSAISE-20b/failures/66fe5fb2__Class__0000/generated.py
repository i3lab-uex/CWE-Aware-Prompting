import json
from configparser import ConfigParser, Error as ConfigError
from typing import Any

# Define the list of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw binary data received from an external source.
    method_format : str
        A string indicating the serialization format used (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object obtained after successful deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the list of safe formats.
    json.JSONDecodeError, configparser.Error
        If the data cannot be parsed according to its format.
    """
    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Deserialization format '{method_format}' is not allowed.")

    if fmt == "json":
        # Decode bytes to string assuming UTF-8 (common default for JSON)
        text = serialized_bytes.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        parser = ConfigParser()
        try:
            # configparser expects a file-like object; use read_string after decoding.
            parser.read_string(serialized_bytes.decode("utf-8"))
        except (ConfigError, UnicodeDecodeError) as exc:
            raise ValueError("Failed to parse INI data") from exc

        # Convert the parsed structure into a plain dict.
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result

    # In practice this point is unreachable because of the SAFE_FORMATS check,
    # but it's good to keep a fallback for static type checkers.
    raise ValueError(f"Unsupported format: {method_format}")