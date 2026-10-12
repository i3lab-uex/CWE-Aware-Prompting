import json
import configparser
from io import StringIO

def load_serialized_content(serialized_input: bytes, serialization_format: str):
    """
    Deserialize binary data from trusted formats only.

    Parameters
    ----------
    serialized_input : bytes
        The binary representation of the data to deserialize.
    serialization_format : str
        One of 'json' or 'ini'. Case-insensitive.

    Returns
    -------
    object
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not recognized or considered unsafe.
    """
    if not isinstance(serialized_input, (bytes, bytearray)):
        raise TypeError("serialized_input must be bytes or bytearray")

    fmt = serialization_format.lower()
    if fmt == 'json':
        # json.loads expects a str, so decode using UTF-8
        try:
            text = serialized_input.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        return json.loads(text)

    elif fmt == 'ini':
        # configparser expects a file-like object containing text
        try:
            text = serialized_input.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for INI") from exc
        parser = configparser.ConfigParser()
        # ConfigParser requires a file-like object; StringIO works.
        parser.read_file(StringIO(text))
        # Convert to a nested dictionary
        return {section: dict(parser.items(section)) for section in parser.sections()}

    else:
        # Any other format is rejected to avoid unsafe deserialization
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")