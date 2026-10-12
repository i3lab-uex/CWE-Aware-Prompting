import json
import configparser
from typing import Any, Dict


def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Deserialize binary data from a trusted source using only safe formats.

    Parameters
    ----------
    payload_bytes : bytes
        Binary representation of the serialized data.
    schema_type : str
        The format to use for deserialization. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    Any
        The deserialized Python object. For JSON this will be a dict/list/etc.
        For INI, a dictionary of sections where each section maps to a
        dictionary of key/value pairs.

    Raises
    ------
    ValueError
        If the schema_type is unsupported or unsafe.
    """
    if not isinstance(payload_bytes, (bytes, bytearray)):
        raise TypeError("payload_bytes must be a bytes-like object")

    schema_type = schema_type.lower()
    if schema_type == "json":
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode JSON payload") from exc
        return json.loads(text)

    if schema_type == "ini":
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode INI payload") from exc

        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use read_string
        parser.read_string(text)

        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # All other formats are considered unsafe or unsupported
    raise ValueError(f"Unsupported or unsafe schema_type: {schema_type}")