import json
import configparser
from io import BytesIO

def safely_deserialize_data(serialized_bytes: bytes, method_format: str):
    """
    Deserialize binary data using only approved formats.

    Args:
        serialized_bytes (bytes): The serialized input.
        method_format (str): The serialization format used ('json' or 'ini').

    Returns:
        object: The deserialized Python object.

    Raises:
        ValueError: If the format is not supported or disallowed.
        json.JSONDecodeError / configparser.Error: For malformed data.
    """
    fmt = method_format.lower()
    if fmt == "json":
        # JSON is safe for data structures (dict, list, str, int, float, bool, None)
        return json.loads(serialized_bytes.decode('utf-8'))

    if fmt == "ini":
        # Parse INI data into a configparser object
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object, so wrap bytes with BytesIO
            parser.read_file(BytesIO(serialized_bytes))
        except Exception as exc:
            raise configparser.Error(f"Failed to parse INI data: {exc}") from exc
        # Convert ConfigParser to a nested dict for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # Disallow unsafe formats such as pickle, marshal, etc.
    raise ValueError(f"Deserialization format '{method_format}' is not allowed or unsupported.")