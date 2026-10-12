import json
import configparser
from io import BytesIO
from typing import Any, Dict


# Define a whitelist of safe formats for deserialization.
SAFE_FORMATS = {
    "json",
    "ini",  # INI files parsed into a nested dictionary.
}


def _parse_ini(data: bytes) -> Dict[str, Dict[str, str]]:
    """
    Parse INI formatted data into a nested dictionary.
    """
    parser = configparser.ConfigParser()
    # ConfigParser expects text; decode using utf-8.
    parser.read_file(BytesIO(data))
    result: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from a trusted format.

    Parameters
    ----------
    byte_data : bytes
        Binary data to be deserialized.
    struct_format : str
        The format used for deserialization (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not recognized or deemed unsafe.
    """
    fmt = struct_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format!r}")

    if fmt == "json":
        # json.loads expects a string; decode using utf-8.
        return json.loads(byte_data.decode("utf-8"))
    elif fmt == "ini":
        return _parse_ini(byte_data)
    else:
        # This branch should never be reached due to the whitelist check.
        raise ValueError(f"Unhandled format: {struct_format!r}")