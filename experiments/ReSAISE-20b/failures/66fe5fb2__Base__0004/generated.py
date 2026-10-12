import json
import configparser
from io import StringIO

def safely_deserialize_data(serialized_bytes: bytes, method_format: str):
    """
    Safely deserialize data from a byte string using only permitted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary data to be deserialized.
    method_format : str
        The serialization format used: 'json' or 'ini'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json", "ini"}

    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: '{method_format}'")

    try:
        if fmt == "json":
            # JSON is safe for basic data structures
            return json.loads(serialized_bytes.decode("utf-8"))
        elif fmt == "ini":
            # ConfigParser loads only simple key/value pairs
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(serialized_bytes.decode("utf-8")))
            result = {}
            for section in parser.sections():
                result[section] = dict(parser.items(section))
            return result
    except Exception as exc:
        raise ValueError(f"Deserialization failed for format '{method_format}': {exc}") from exc