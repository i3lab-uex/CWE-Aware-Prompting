import json
import configparser
from io import StringIO

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Deserialize binary payloads that come from external sources using only
    safe and curated formats.

    Parameters:
        payload_bytes (bytes): The binary data to deserialize.
        schema_type (str): One of the supported formats: 'json' or 'ini'.

    Returns:
        The Python object obtained after deserialization.

    Raises:
        ValueError: If the format is unsupported or unsafe.
        json.JSONDecodeError: If JSON decoding fails.
    """
    # Normalise the schema_type to lower case for comparison
    fmt = schema_type.lower()

    if fmt == "json":
        # JSON is safe for deserialization when the input is validated as UTF‑8
        text = payload_bytes.decode("utf-8")
        return json.loads(text)

    elif fmt == "ini":
        # ConfigParser reads INI files into a sectioned dictionary.
        text = payload_bytes.decode("utf-8")
        parser = configparser.ConfigParser()
        # Avoid interpolation for safety
        parser.read_file(StringIO(text))
        config = {}
        for section in parser.sections():
            config[section] = dict(parser.items(section))
        return config

    else:
        # Any other format is considered unsafe or unsupported
        raise ValueError(f"Unsupported or unsafe deserialization format: {schema_type}")