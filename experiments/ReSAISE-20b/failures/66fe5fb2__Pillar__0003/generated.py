import json
import configparser
from typing import Any, Dict

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json",
    "ini",  # INI files parsed with configparser
}

class UnsafeFormatError(ValueError):
    """Raised when an unsupported or unsafe format is requested."""


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize binary data safely based on a controlled list of formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary payload to deserialize.
    method_format : str
        The format used for serialization (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    UnsafeFormatError
        If the requested format is not in the allowed list.
    ValueError
        If the data cannot be parsed for the requested format.
    """
    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise UnsafeFormatError(f"Deserialization format '{method_format}' is not permitted.")

    # Decode bytes to a string assuming UTF‑8. Raise if decoding fails.
    try:
        decoded = serialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Failed to decode bytes as UTF‑8.") from exc

    if fmt == "json":
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser requires a file-like object; use read_string within a context manager.
        try:
            parser.read_string(decoded)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data.") from exc
        # Convert to a nested dictionary for easier consumption.
        config_dict: Dict[str, Dict[str, str]] = {
            section: dict(parser[section]) for section in parser.sections()
        }
        return config_dict

    # The code path should never reach here because of the SAFE_FORMATS check.
    raise UnsafeFormatError(f"Unhandled format: {method_format}")