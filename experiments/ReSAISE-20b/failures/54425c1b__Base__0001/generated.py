import json
import configparser
from io import BytesIO

# List of allowed serialization formats.
ALLOWED_FORMATS = {"json", "ini"}

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Deserialize binary data safely using only permitted formats.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary format.
    format_type : str
        Serialization mechanism used ('json', 'ini').

    Returns
    -------
    object
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS.
    json.JSONDecodeError, configparser.Error
        If the data cannot be parsed with the chosen format.
    """
    if not isinstance(data_input, (bytes, bytearray)):
        raise TypeError("data_input must be bytes or bytearray")

    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {format_type!r}")

    # Decode bytes to string safely (utf-8 is common for json/ini)
    try:
        text = data_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data could not be decoded using UTF-8") from exc

    if fmt == "json":
        # json.loads is safe for primitive data types; it does not execute code.
        return json.loads(text)

    if fmt == "ini":
        # ConfigParser reads INI files into a dictionary-like structure.
        parser = configparser.ConfigParser()
        # ConfigParser expects file-like objects; use BytesIO.
        parser.read_file(BytesIO(text.encode("utf-8")))
        # Convert to a plain dict for easier use.
        return {section: dict(parser[section]) for section in parser.sections()}

    # This point should never be reached due to the ALLOWED_FORMATS check.
    raise ValueError(f"Unhandled format: {format_type!r}")