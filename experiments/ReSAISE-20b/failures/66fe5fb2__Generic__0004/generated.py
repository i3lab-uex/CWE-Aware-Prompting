import json
import configparser
from typing import Any

# Define the list of formats that are considered safe.
SAFE_FORMATS = {"json", "ini"}

def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Safely deserialize binary data based on the specified format.

    Parameters
    ----------
    serialized_bytes : bytes
        Binary representation of the data to deserialize.
    method_format : str
        Serialization format used (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the list of allowed formats.
    """
    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Deserialization format '{method_format}' is not allowed.")

    if fmt == "json":
        try:
            return json.loads(serialized_bytes.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data.") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; we use a BytesIO wrapper.
            from io import StringIO
            parser.read_file(StringIO(serialized_bytes.decode("utf-8")))
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Failed to deserialize INI data.") from exc

        # Convert the ConfigParser object into a plain dictionary.
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # The code should never reach here due to the earlier check, but keep for completeness.
    raise ValueError(f"Unhandled serialization format: {method_format}")