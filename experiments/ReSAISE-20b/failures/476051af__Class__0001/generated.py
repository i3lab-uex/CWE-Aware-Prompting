import json
import configparser
from io import StringIO

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Safely deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    bin_data : bytes
        Binary representation of the serialized data.
    format_type : str
        The serialization format. Supported values are:
            * 'json'  – JSON encoded data.
            * 'ini'   – INI configuration file.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not supported or unsafe.
    """
    # Decode bytes to string safely
    try:
        text = bin_data.decode('utf-8')
    except Exception as exc:
        raise ValueError("Failed to decode binary data as UTF-8") from exc

    fmt = format_type.lower()
    if fmt == 'json':
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == 'ini':
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(StringIO(text))
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert to a nested dictionary
        config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
        return config_dict

    # Disallow pickle and any other formats
    raise ValueError(f"Unsupported or unsafe format: {format_type}")