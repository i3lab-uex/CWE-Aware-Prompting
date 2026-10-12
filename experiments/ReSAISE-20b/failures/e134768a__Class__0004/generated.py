import json
import configparser
from typing import Any, Union

# Define the set of safe formats that are allowed for deserialization
SAFE_FORMATS = {"json", "ini"}

def unpack_serialized_object(byte_data: bytes, struct_format: str) -> Any:
    """
    Deserialize binary data from a trusted source using only predefined safe formats.

    Parameters
    ----------
    byte_data : bytes
        The binary data to deserialize.
    struct_format : str
        The format identifier used for deserialization. Must be one of the
        values in SAFE_FORMATS.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the provided format is not recognized or deemed unsafe.
    """
    if not isinstance(byte_data, (bytes, bytearray)):
        raise TypeError("byte_data must be bytes or bytearray")

    fmt = struct_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format '{struct_format}'. "
                         f"Allowed formats: {', '.join(SAFE_FORMATS)}")

    # Decode the bytes to a string for text-based formats
    try:
        data_str = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("byte_data is not valid UTF-8 encoded text") from exc

    if fmt == "json":
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # configparser expects a file-like object
            parser.read_string(data_str)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the ConfigParser object to a nested dictionary
        result: dict[str, dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point should never be reached due to the format check above
    raise RuntimeError("Unhandled deserialization path")