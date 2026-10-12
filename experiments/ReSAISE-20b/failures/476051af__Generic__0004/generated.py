import json
import configparser

class UnsupportedFormatError(RuntimeError):
    """Raised when an unsupported or unsafe format is requested."""
    pass

def deserialize_binary_data(bin_data: bytes, format_type: str):
    """
    Safely deserializes binary data from a trusted source.

    Parameters
    ----------
    bin_data : bytes
        The serialized data in binary form.
    format_type : str
        One of 'json', 'ini' (case-insensitive). Other formats are rejected.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    UnsupportedFormatError
        If the format is unsupported or unsafe (e.g., 'pickle').
    ValueError
        If the data cannot be parsed according to the requested format.
    """
    if not isinstance(bin_data, (bytes, bytearray)):
        raise TypeError("bin_data must be bytes or bytearray")

    fmt = format_type.lower()

    if fmt == "json":
        # JSON is safe for deserialization as it only creates basic data types.
        try:
            return json.loads(bin_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    elif fmt == "ini":
        # INI files are parsed into a ConfigParser object; we return a dict for convenience.
        parser = configparser.ConfigParser()
        try:
            parser.read_string(bin_data.decode("utf-8"))
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Failed to parse INI data") from exc
        # Convert ConfigParser to a nested dictionary.
        config_dict = {section: dict(parser.items(section)) for section in parser.sections()}
        return config_dict

    else:
        # Any other format (including 'pickle') is considered unsafe or unsupported.
        raise UnsupportedFormatError(f"Deserialization of format '{format_type}' is not supported.")