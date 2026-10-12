import json
import configparser
from io import BytesIO

# Define the set of trusted formats that are allowed for deserialization.
ALLOWED_FORMATS = {"json", "ini"}


def decode_serialized_data(data_bytes: bytes, format_string: str):
    """
    Safely deserialize binary data according to a trusted format.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format (e.g. 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or untrusted.
    """
    if format_string.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string}")

    if format_string.lower() == "json":
        # json.loads expects a str, so decode bytes to UTF-8.
        return json.loads(data_bytes.decode("utf-8"))

    if format_string.lower() == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; BytesIO allows us to read from bytes.
        parser.read_file(BytesIO(data_bytes))
        # Convert the ConfigParser object into a plain dictionary.
        return {section: dict(parser[section]) for section in parser.sections()}

    # This point should never be reached because of the ALLOWED_FORMATS check.
    raise ValueError(f"Unhandled format: {format_string}")