import json
import configparser
from io import BytesIO

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Deserialize binary payloads from a restricted set of safe formats.

    Parameters
    ----------
    payload_bytes : bytes
        Binary data to be deserialized.
    schema_type : str
        One of 'json' or 'ini'.  Other values raise an exception.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the schema_type is unsupported or unsafe.
    """
    if not isinstance(payload_bytes, (bytes, bytearray)):
        raise TypeError("payload_bytes must be bytes-like")

    schema_type = schema_type.lower()
    if schema_type == "json":
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    elif schema_type == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(BytesIO(payload_bytes))
        except configparser.Error as exc:
            raise ValueError("Malformed INI data") from exc

        # Convert to a nested dictionary: {section: {key: value}}
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    else:
        # pickle and other formats are intentionally disallowed
        raise ValueError(f"Unsupported or unsafe schema_type: {schema_type}")