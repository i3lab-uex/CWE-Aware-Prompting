import json
import configparser
from typing import Any


def process_serialized_content(payload_bytes: bytes, schema_type: str) -> Any:
    """
    Deserialize binary data using a safe, curated set of formats.

    Parameters
    ----------
    payload_bytes : bytes
        The binary representation of the serialized data.
    schema_type : str
        The format used for serialization. Supported values are:
            - 'json'  : JSON text
            - 'ini'   : INI configuration text

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the schema_type is unsupported or considered unsafe.
    """
    # Ensure we have a supported format
    safe_formats = {"json", "ini"}
    if schema_type not in safe_formats:
        raise ValueError(f"Unsupported or unsafe deserialization format: {schema_type}")

    try:
        # Decode the payload assuming UTF-8; errors will raise an exception
        text = payload_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Payload bytes are not valid UTF-8 encoded text") from exc

    if schema_type == "json":
        # JSON is safe for deserialization when using json.loads
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON payload") from exc

    if schema_type == "ini":
        # INI parsing is safe; we use ConfigParser to parse the text
        parser = configparser.ConfigParser()
        try:
            parser.read_string(text)
        except (configparser.Error, ValueError) as exc:
            raise ValueError("Invalid INI payload") from exc
        # Convert to a simple dict representation
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result