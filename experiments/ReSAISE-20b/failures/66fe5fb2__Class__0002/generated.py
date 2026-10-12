import json
import configparser
from typing import Any, Dict


# A whitelist of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize binary data safely using only permitted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        Binary representation of the serialized data.
    method_format : str
        The serialization format used (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not allowed or supported.
    """
    fmt = method_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Format '{method_format}' is not allowed or supported.")

    if fmt == "json":
        # Decode bytes to string safely using UTF-8; errors='strict' will raise if invalid.
        text = serialized_bytes.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        # ConfigParser expects a file-like object; use a StringIO.
        config = configparser.ConfigParser()
        text = serialized_bytes.decode("utf-8")
        from io import StringIO
        config.read_file(StringIO(text))
        # Convert to a plain dictionary for easier use.
        result: Dict[str, Dict[str, str]] = {}
        for section in config.sections():
            result[section] = dict(config.items(section))
        return result

    # This point is unreachable due to the whitelist check, but kept for completeness.
    raise ValueError(f"Unhandled format: {method_format}")