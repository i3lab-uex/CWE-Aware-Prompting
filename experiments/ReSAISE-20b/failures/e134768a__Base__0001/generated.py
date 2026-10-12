import json
import configparser
from typing import Any, Dict

# Allowed formats for deserialization.  Only these are considered safe.
ALLOWED_FORMATS = {"json", "ini"}


def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source only if the format is in
    a predefined whitelist of safe formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        The format of the data, e.g. 'json', 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = struct_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {struct_format}")

    try:
        if fmt == "json":
            # Decode bytes to string assuming UTF‑8 (common for JSON)
            text = byte_data.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            # Parse INI data using configparser.  The result is a dictionary
            # of sections, each containing a dict of key/value pairs.
            parser = configparser.ConfigParser()
            # configparser expects a file-like object; use StringIO
            from io import StringIO

            parser.read_file(StringIO(byte_data.decode("utf-8")))
            result: Dict[str, Dict[str, str]] = {}
            for section in parser.sections():
                result[section] = dict(parser.items(section))
            return result

    except Exception as exc:
        # Wrap any exception from the deserialization step
        raise ValueError(f"Deserialization failed for format '{struct_format}': {exc}") from exc