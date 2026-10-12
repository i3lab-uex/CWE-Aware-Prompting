import json
import configparser
from typing import Any, Dict

def deserialize_binary_data(bin_data: bytes, format_type: str) -> Any:
    """
    Safely deserialize binary data into a Python object.

    Parameters
    ----------
    bin_data : bytes
        Serialized data in binary form.
    format_type : str
        The serialization format. Supported values are:
            - 'json'  : JSON data (text-based).
            - 'ini'   : INI configuration file.
        Other formats are considered unsafe or unsupported.

    Returns
    -------
    Any
        The Python object obtained after deserialization.
        For 'json' this will be a native JSON structure (dict, list, etc.).
        For 'ini' this will be a nested dictionary mapping section names to key/value pairs.

    Raises
    ------
    ValueError
        If the format_type is unsupported or unsafe.
    json.JSONDecodeError, configparser.Error
        Propagated if the data cannot be parsed for the chosen format.
    """
    # Ensure the input is bytes
    if not isinstance(bin_data, (bytes, bytearray)):
        raise TypeError("bin_data must be bytes-like")

    fmt = format_type.lower()
    if fmt == "json":
        # JSON is text-based; decode using UTF-8
        try:
            text = bin_data.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError("JSON data is not valid UTF-8") from e
        return json.loads(text)

    if fmt == "ini":
        # INI is also text-based; decode using UTF-8
        try:
            text = bin_data.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError("INI data is not valid UTF-8") from e

        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use read_string
        parser.read_string(text)

        # Convert the ConfigParser data into a plain dictionary
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Any other format is considered unsafe or unsupported
    raise ValueError(f"Unsupported or unsafe deserialization format: {format_type}")