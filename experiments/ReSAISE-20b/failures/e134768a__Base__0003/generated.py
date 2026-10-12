import json
import configparser
from io import StringIO
from typing import Any, Dict


# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}


def _parse_ini(data: bytes) -> Dict[str, Dict[str, str]]:
    """
    Parse INI formatted data and return a nested dictionary.

    Parameters
    ----------
    data : bytes
        The raw INI data as bytes.

    Returns
    -------
    dict
        A dictionary where each key is a section name and the value is another
        dictionary of option/value pairs.
    """
    parser = configparser.ConfigParser()
    # ConfigParser expects a text stream; decode using UTF‑8.
    parser.read_file(StringIO(data.decode("utf-8")))
    result = {}
    for section in parser.sections():
        result[section] = dict(parser.items(section))
    return result


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using only
    predefined safe formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to be deserialized.
    struct_format : str
        The format used for deserialization. Supported values are:
        'json' and 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the set of safe formats or if
        deserialization fails.
    """
    fmt = struct_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format}")

    try:
        if fmt == "json":
            # json.loads expects a str; decode using UTF‑8.
            return json.loads(byte_data.decode("utf-8"))
        elif fmt == "ini":
            return _parse_ini(byte_data)
    except Exception as exc:
        # Wrap any exception into a ValueError to keep the API simple.
        raise ValueError(f"Failed to deserialize data as {struct_format}: {exc}") from exc