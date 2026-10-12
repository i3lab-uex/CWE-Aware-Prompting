import json
import configparser
from io import BytesIO


def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Safely deserializes binary data using only supported formats.

    Parameters
    ----------
    bin_data : bytes
        Serialized data in binary form.
    format_type : str
        The serialization format to use. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is unsupported or unsafe.
    """
    if not isinstance(bin_data, (bytes, bytearray)):
        raise TypeError("bin_data must be a bytes-like object")

    fmt = format_type.lower()

    if fmt == "json":
        try:
            # Decode UTF-8 and parse JSON
            return json.loads(bin_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(BytesIO(bin_data))
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the parser to a plain dict
        return {section: dict(parser[section]) for section in parser.sections()}

    # Any other format is considered unsupported/unsafe
    raise ValueError(f"Unsupported or unsafe format: {format_type}")