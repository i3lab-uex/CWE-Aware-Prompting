import json
import configparser
from io import StringIO


# Define the list of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}


def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Safely deserialize binary data received from an untrusted source.

    Parameters
    ----------
    byte_data : bytes
        Serialized data in binary form.
    serialization_format : str
        The format used to serialize the data. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    object
        The Python representation of the deserialized data.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS.
    json.JSONDecodeError
        If JSON data cannot be decoded.
    configparser.Error
        If INI data is malformed.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Deserialization format '{serialization_format}' is not allowed.")

    if fmt == "json":
        # JSON is safe as it only constructs basic Python types.
        return json.loads(byte_data.decode("utf-8"))

    if fmt == "ini":
        # INI files are parsed into a ConfigParser object.
        parser = configparser.ConfigParser()
        # ConfigParser expects text, so decode the bytes first.
        parser.read_file(StringIO(byte_data.decode("utf-8")))
        # Convert the ConfigParser into a plain dictionary for easier use.
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result