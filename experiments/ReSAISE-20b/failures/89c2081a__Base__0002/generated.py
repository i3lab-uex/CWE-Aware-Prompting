import json
import configparser
from io import BytesIO

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Safely deserialize binary data based on a curated list of formats.

    Parameters
    ----------
    payload_bytes : bytes
        Binary representation of the serialized data.
    schema_type : str
        The format used for serialization. Supported values are:
            - 'json'  : JSON data
            - 'ini'   : INI configuration

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    ValueError
        If the requested format is unsupported or considered unsafe.
    """
    # Ensure we only support explicitly safe formats
    safe_formats = {'json', 'ini'}
    if schema_type not in safe_formats:
        raise ValueError(f"Unsupported or unsafe format: {schema_type!r}")

    if schema_type == 'json':
        # JSON is safe when we use json.loads with a string
        try:
            text = payload_bytes.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("JSON payload is not valid UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON payload") from exc

    # schema_type == 'ini'
    config = configparser.ConfigParser()
    try:
        with BytesIO(payload_bytes) as f:
            config.read_file(f)
    except (configparser.Error, UnicodeDecodeError) as exc:
        raise ValueError("Invalid INI payload") from exc

    # Convert ConfigParser to a plain dict
    result = {section: dict(config[section]) for section in config.sections()}
    return result