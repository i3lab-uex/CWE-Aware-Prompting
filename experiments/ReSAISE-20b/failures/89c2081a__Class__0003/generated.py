import json
import configparser
from typing import Any

def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Deserialize binary payloads safely according to a whitelisted schema type.

    Parameters
    ----------
    payload_bytes : bytes
        The binary data to deserialize.
    schema_type : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the schema_type is unsupported or if deserialization fails.
    """
    # Ensure we only handle known safe formats
    schema_type = schema_type.lower()
    if schema_type == 'json':
        try:
            text = payload_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON payload") from exc

    elif schema_type == 'ini':
        try:
            text = payload_bytes.decode('utf-8')
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(text)
            # Convert to a dictionary of dictionaries for ease of use
            return {section: dict(parser[section]) for section in parser.sections()}
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Failed to deserialize INI payload") from exc

    else:
        # Any other format is considered unsafe or unsupported
        raise ValueError(f"Unsupported schema type: {schema_type!r}")