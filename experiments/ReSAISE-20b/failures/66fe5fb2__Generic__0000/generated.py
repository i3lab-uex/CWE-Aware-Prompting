import json
import configparser
from io import BytesIO
from typing import Any, Dict


# A set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}


def _deserialize_json(data: bytes) -> Any:
    """Deserialize JSON data from bytes."""
    text = data.decode("utf-8")
    return json.loads(text)


def _deserialize_ini(data: bytes) -> Dict[str, Dict[str, str]]:
    """Deserialize INI data from bytes into a nested dictionary."""
    parser = configparser.ConfigParser()
    # ConfigParser expects a file-like object. BytesIO provides that.
    parser.read_file(BytesIO(data))
    # Convert the ConfigParser object to a plain dict of dicts.
    result: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize incoming binary data in a safe manner.

    Parameters
    ----------
    serialized_bytes : bytes
        Binary representation of the data to deserialize.
    method_format : str
        The format that was used during serialization. Supported values are
        'json' and 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not in the list of safe formats or if deserialization fails.
    """
    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Deserialization format '{method_format}' is not allowed.")

    try:
        if fmt == "json":
            return _deserialize_json(serialized_bytes)
        elif fmt == "ini":
            return _deserialize_ini(serialized_bytes)
    except Exception as exc:
        raise ValueError(f"Failed to deserialize data using format '{method_format}': {exc}") from exc