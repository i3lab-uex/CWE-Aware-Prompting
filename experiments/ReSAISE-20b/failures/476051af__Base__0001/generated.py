import json
import configparser
from io import StringIO

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Deserialize binary data into a Python object using only safe formats.

    Parameters
    ----------
    bin_data : bytes
        The serialized data in binary form.
    format_type : str
        One of the supported formats: 'json' or 'ini'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    if not isinstance(bin_data, bytes):
        raise TypeError("bin_data must be a bytes object")

    fmt = format_type.lower()

    if fmt == "json":
        try:
            text = bin_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        try:
            text = bin_data.decode("utf-8")
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(text))
            # Convert to a plain dict for easier consumption
            return {section: dict(parser[section]) for section in parser.sections()}
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI data") from exc

    # Reject any other format, including pickle which is unsafe
    raise ValueError(f"Unsupported or unsafe format: {format_type}")