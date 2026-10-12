import json
import configparser
from io import StringIO

def deserialize_payload(byte_sequence: bytes, data_format: str):
    """
    Deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to be deserialized.
    data_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    object
        The Python representation of the data.

    Raises
    ------
    ValueError
        If the format is unsupported or deserialization fails.
    """
    if not isinstance(byte_sequence, bytes):
        raise TypeError("byte_sequence must be of type 'bytes'")

    format_lower = data_format.lower()

    # Decode bytes to text using UTF-8 (common for JSON and INI)
    try:
        text = byte_sequence.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes are not valid UTF-8") from exc

    if format_lower == "json":
        try:
            # json.loads already protects against code execution
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if format_lower == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(StringIO(text))
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the ConfigParser to a nested dictionary
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # Unsupported format
    raise ValueError(f"Unsupported or unsafe data format: {data_format}")