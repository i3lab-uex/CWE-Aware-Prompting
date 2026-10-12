import json
import configparser
from typing import Any

# Define the set of safe, supported serialization formats.
SAFE_FORMATS = {
    "json": "json",
    "ini": "ini",
}

def load_serialized_content(
    serialized_input: bytes, serialization_format: str
) -> Any:
    """
    Deserialize binary data from an untrusted source, only allowing safe formats.

    Parameters
    ----------
    serialized_input : bytes
        The binary data to deserialize.
    serialization_format : str
        The format used for deserialization. Supported values are
        'json' and 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not recognized or deemed unsafe.
    json.JSONDecodeError
        For malformed JSON data.
    configparser.Error
        For malformed INI data.

    Notes
    -----
    This function intentionally avoids pickle, yaml, marshal and other
    formats that can execute arbitrary code during deserialization.
    """
    fmt = SAFE_FORMATS.get(serialization_format.lower())
    if not fmt:
        raise ValueError(
            f"Unsupported or unsafe serialization format: {serialization_format!r}"
        )

    if fmt == "json":
        # Decode bytes to str using UTF-8 and parse JSON.
        text = serialized_input.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        # Parse INI into a nested dictionary.
        text = serialized_input.decode("utf-8")
        parser = configparser.ConfigParser()
        parser.read_string(text)
        result: dict[str, dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # In practice this point is unreachable because of the guard above.
    raise ValueError(f"Unhandled format: {serialization_format!r}")