import json
import configparser
from io import StringIO


def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Deserialize binary data that has been encoded in a known safe format.

    Parameters
    ----------
    bin_data : bytes
        The serialized data in binary form.
    format_type : str
        One of the supported, safe formats: 'json', 'ini'.

    Returns
    -------
    object
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is unsupported or deemed unsafe.
    """
    if not isinstance(bin_data, (bytes, bytearray)):
        raise TypeError("bin_data must be bytes or bytearray")

    fmt = format_type.lower()
    if fmt == "json":
        # JSON is safe as long as we use json.loads on a string.
        text = bin_data.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        # ConfigParser parses INI files into a dict-like structure.
        text = bin_data.decode("utf-8")
        parser = configparser.ConfigParser()
        parser.read_file(StringIO(text))
        # Convert to a plain dictionary for easier consumption.
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # Any other format is considered unsafe or unsupported.
    raise ValueError(f"Unsupported or unsafe format_type: {format_type}")