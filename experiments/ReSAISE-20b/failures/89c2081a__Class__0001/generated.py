import json
from configparser import ConfigParser
from io import BytesIO

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Deserialize binary payloads safely.

    Parameters
    ----------
    payload_bytes : bytes
        Binary data representing the serialized content.
    schema_type : str
        The serialization format. Supported values are:
            - 'json'   : JSON text encoded in UTF‑8.
            - 'ini'    : INI configuration file format.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    # Normalise schema_type to lower case
    fmt = schema_type.strip().lower()

    if fmt == 'json':
        try:
            text = payload_bytes.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("JSON payload must be UTF‑8 encoded") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == 'ini':
        parser = ConfigParser()
        try:
            # ConfigParser expects a file‑like object
            parser.read_file(BytesIO(payload_bytes))
        except Exception as exc:
            raise ValueError("Invalid INI data") from exc
        # Convert to a plain dict for easier use
        config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
        return config_dict

    else:
        # Reject any other format, including pickle or eval‑based formats
        raise ValueError(f"Unsupported or unsafe serialization format: {schema_type}")