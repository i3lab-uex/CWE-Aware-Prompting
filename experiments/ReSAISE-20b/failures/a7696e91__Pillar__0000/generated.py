import json
import configparser
from io import StringIO
from typing import Any, Dict

# A whitelist of safe serialization formats.
SAFE_FORMATS = {"json", "ini"}


def load_serialized_content(serialized_input: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source.

    Parameters
    ----------
    serialized_input : bytes
        Binary representation of the serialized data.
    serialization_format : str
        The format used for deserialization. Supported values are 'json' and 'ini'.

    Returns
    -------
    Any
        The Python object represented by the input data.

    Raises
    ------
    ValueError
        If `serialization_format` is not in the whitelist of safe formats.
    json.JSONDecodeError
        If JSON data cannot be decoded.
    configparser.Error
        If INI data is malformed.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    # Convert bytes to a text string using UTF‑8.  Errors are replaced to avoid
    # raising during decoding of malformed data.
    text = serialized_input.decode("utf-8", errors="replace")

    if fmt == "json":
        # json.loads is safe for primitive data types; it does not execute code.
        return json.loads(text)

    if fmt == "ini":
        # ConfigParser reads INI files into a dictionary‑like object.
        parser = configparser.ConfigParser()
        # ConfigParser expects file‑like objects; StringIO provides that.
        parser.read_file(StringIO(text))
        # Convert to a plain dict for easier consumption.
        return {section: dict(parser[section]) for section in parser.sections()}


# Example usage (commented out to keep the module importable without side effects)
# if __name__ == "__main__":
#     json_bytes = b'{"key": "value"}'
#     ini_bytes = b'[section]\nfoo=bar\n'
#
#     print(load_serialized_content(json_bytes, "json"))
#     print(load_serialized_content(ini_bytes, "ini"))