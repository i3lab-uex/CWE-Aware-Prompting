import json
import configparser
from io import BytesIO


def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Safely deserializes binary data using a restricted set of formats.

    Parameters
    ----------
    data_input : bytes
        The serialized data received in binary format.
    format_type : str
        One of the allowed serialization formats: 'json', 'ini'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or not allowed.
    """
    # Normalise the format string
    fmt = format_type.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to str using UTF-8
            text = data_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON data") from exc

    if fmt == "ini":
        # INI files are parsed into a ConfigParser instance.
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(BytesIO(data_input))
        except configparser.Error as exc:
            raise ValueError("Failed to parse INI data") from exc

        # Convert the ConfigParser into a plain dictionary
        config_dict = {}
        for section in parser.sections():
            config_dict[section] = dict(parser.items(section))
        return config_dict

    # Disallow any other formats (e.g., pickle, yaml, etc.) to avoid
    # security risks such as arbitrary code execution.
    raise ValueError(f"Unsupported or disallowed format: {format_type}")