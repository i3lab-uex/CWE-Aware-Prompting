import json
import configparser
from typing import Any

class UnsupportedSchemaError(RuntimeError):
    """Raised when an unsupported or unsafe schema type is requested."""
    pass

def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Deserialize binary payloads using a curated set of safe formats.

    Parameters
    ----------
    payload_bytes : bytes
        Binary data to deserialize.
    schema_type : str
        One of the supported schema types: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    UnsupportedSchemaError
        If the requested schema is unsupported or unsafe.
    ValueError
        If the payload cannot be decoded or parsed for the given schema.
    """
    # Ensure schema_type is a string and lower‑case it
    if not isinstance(schema_type, str):
        raise UnsupportedSchemaError("schema_type must be a string")

    schema = schema_type.strip().lower()

    # Decode bytes to text; reject if decoding fails
    try:
        text = payload_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Unable to decode payload_bytes: {exc}") from exc

    if schema == "json":
        try:
            return json.loads(text, strict=True)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON payload: {exc}") from exc

    if schema == "ini":
        parser = configparser.ConfigParser()
        try:
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError(f"Invalid INI payload: {exc}") from exc

        # Convert ConfigParser to a plain dict for easier consumption
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Any other schema is considered unsafe or unsupported
    raise UnsupportedSchemaError(
        f"Unsupported or unsafe schema_type: '{schema_type}'. "
        "Only 'json' and 'ini' are allowed."
    )