import json
import configparser
from io import StringIO

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Deserialize binary data safely for a limited set of formats.

    Parameters
    ----------
    bin_data : bytes
        The binary representation of the serialized data.
    format_type : str
        One of 'json', 'ini'. Other values raise an exception.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is unsupported or unsafe.
    """
    if not isinstance(bin_data, bytes):
        raise TypeError("bin_data must be of type 'bytes'")

    fmt = format_type.lower()
    if fmt == "json":
        # JSON is safe for deserialization
        try:
            text = bin_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        # configparser reads INI files into a dictionary-like structure
        try:
            text = bin_data.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(text))
            # Convert to a plain dict for easier consumption
            result = {section: dict(parser[section]) for section in parser.sections()}
            return result
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI data") from exc

    # Disallow potentially unsafe formats such as pickle
    raise ValueError(f"Unsupported or unsafe format: {format_type}")