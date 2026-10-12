import json
import configparser
from typing import Any, Dict

# Define the set of trusted formats that are safe to deserialize.
ALLOWED_FORMATS = {"json", "ini"}

def _parse_ini(data_bytes: bytes) -> Dict[str, Any]:
    """
    Parse INI data into a dictionary. The configparser module only
    handles plain key/value pairs and does not execute arbitrary code.
    """
    config = configparser.ConfigParser()
    # ConfigParser expects a file-like object; we wrap the bytes in BytesIO.
    from io import StringIO
    # Decode as UTF-8; errors='strict' will raise if the bytes are not valid UTF‑8.
    text = data_bytes.decode("utf-8", errors="strict")
    config.read_file(StringIO(text))

    result: Dict[str, Any] = {}
    for section in config.sections():
        result[section] = dict(config.items(section))
    return result

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize `data_bytes` according to the trusted `format_string`.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary format.
    format_string : str
        Identifier of the serialization format. Must be one of the
        trusted formats defined in ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object. For JSON it may be a dict, list,
        etc. For INI it will always be a dictionary mapping section names
        to dictionaries of key/value pairs.

    Raises
    ------
    ValueError
        If `format_string` is not in ALLOWED_FORMATS or if the data cannot
        be parsed by the chosen format.
    """
    fmt = format_string.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    try:
        if fmt == "json":
            # json.loads expects a str; decode bytes safely.
            text = data_bytes.decode("utf-8", errors="strict")
            return json.loads(text)
        elif fmt == "ini":
            return _parse_ini(data_bytes)
    except (UnicodeDecodeError, json.JSONDecodeError, configparser.Error) as exc:
        # Wrap any parsing exception into a ValueError to keep the API
        # consistent and avoid leaking implementation details.
        raise ValueError(f"Failed to parse data as {format_string!r}: {exc}") from exc