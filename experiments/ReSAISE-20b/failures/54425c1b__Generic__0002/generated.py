import json
import configparser
from io import BytesIO

# List of formats that are considered safe for deserialization
ALLOWED_FORMATS = {"json", "ini"}

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Deserialize binary data safely based on the specified format.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary format.
    format_type : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    object
        The Python representation of the data.

    Raises
    ------
    ValueError
        If `format_type` is not in the allowed list.
    json.JSONDecodeError, configparser.Error
        If the data cannot be parsed by the chosen format.
    """
    if not isinstance(data_input, (bytes, bytearray)):
        raise TypeError("data_input must be bytes or bytearray")

    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Format '{format_type}' is not allowed or supported")

    if fmt == "json":
        # Decode bytes to string using UTF-8; raise UnicodeDecodeError if invalid
        text = data_input.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        # Use ConfigParser to parse the INI data
        parser = configparser.ConfigParser()
        # read_file expects a file-like object; BytesIO provides that
        parser.read_file(BytesIO(data_input))
        # Convert the ConfigParser object into a nested dictionary
        config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
        return config_dict

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_type}")