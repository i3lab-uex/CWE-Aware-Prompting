import json
import configparser
from io import StringIO
from typing import Any


def deserialize_binary_data(bin_data: bytes, format_type: str) -> Any:
    """
    Deserialize binary data from a trusted source.

    Parameters
    ----------
    bin_data : bytes
        Serialized data in binary form.
    format_type : str
        Format of the serialized data. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    Any
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
        # Decode bytes to str safely
        try:
            text = bin_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON data") from exc

    elif fmt == "ini":
        # Use ConfigParser which only parses plain configuration
        parser = configparser.ConfigParser()
        try:
            text = bin_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for INI deserialization") from exc

        try:
            parser.read_file(StringIO(text))
        except configparser.Error as exc:
            raise ValueError("Failed to parse INI data") from exc

        # Convert ConfigParser structure into a plain dict
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    else:
        # Reject any other format to avoid unsafe deserialization
        raise ValueError(
            f"Unsupported or unsafe serialization format: '{format_type}'. "
            "Only 'json' and 'ini' are allowed."
        )