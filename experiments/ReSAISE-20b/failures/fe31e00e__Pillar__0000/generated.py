import json
import configparser
from io import StringIO

def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Safely deserialize binary data using only a whitelisted set of formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data received in binary form.
    serialization_format : str
        The name of the serialization format used. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or if deserialization fails.
    """
    # Convert bytes to text using UTF‑8; raise if decoding fails
    try:
        text = byte_data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data is not valid UTF‑8") from exc

    fmt = serialization_format.lower()

    if fmt == 'json':
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON") from exc

    if fmt == 'ini':
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(StringIO(text))
        except (configparser.Error, ValueError) as exc:
            raise ValueError("Failed to parse INI data") from exc
        # Convert the ConfigParser object into a plain dictionary
        return {section: dict(parser[section]) for section in parser.sections()}

    # Any other format is disallowed
    raise ValueError(f"Deserialization for '{serialization_format}' is not supported or allowed.")