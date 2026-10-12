import json
import configparser
from io import StringIO

def process_serialized_content(payload_bytes: bytes, schema_type: str):
    """
    Deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    payload_bytes : bytes
        The binary representation of the serialized data.
    schema_type : str
        One of 'json' or 'ini'.  Other values raise a ValueError.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or deemed unsafe.
    """
    if not isinstance(payload_bytes, (bytes, bytearray)):
        raise TypeError("payload_bytes must be bytes or bytearray")

    fmt = schema_type.lower()
    if fmt == "json":
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON payload") from exc

    elif fmt == "ini":
        try:
            text = payload_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for INI") from exc
        parser = configparser.ConfigParser()
        try:
            parser.read_file(StringIO(text))
        except configparser.Error as exc:
            raise ValueError("Invalid INI payload") from exc
        # Convert to a plain dict for ease of use
        return {section: dict(parser[section]) for section in parser.sections()}

    else:
        # Any other format is considered unsafe or unsupported
        raise ValueError(f"Unsupported or unsafe schema_type: {schema_type}")