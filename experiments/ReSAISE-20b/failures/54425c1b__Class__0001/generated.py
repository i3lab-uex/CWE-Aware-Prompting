import json
import configparser
from io import BytesIO

# List of allowed formats for deserialization
ALLOWED_FORMATS = {"json", "ini"}

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Deserialize binary data safely based on a permitted format.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary form.
    format_type : str
        The serialization mechanism used: 'json' or 'ini'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS.
    TypeError
        If data_input is not a bytes-like object.
    """
    if not isinstance(data_input, (bytes, bytearray)):
        raise TypeError("data_input must be a bytes-like object")

    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {format_type}")

    if fmt == "json":
        # JSON is text-based; decode bytes to string
        try:
            decoded = data_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        # ConfigParser expects a file-like object
        parser = configparser.ConfigParser()
        try:
            with BytesIO(data_input) as stream:
                parser.read_file(stream)
        except (configparser.Error, UnicodeDecodeError) as exc:
            raise ValueError("Invalid INI data") from exc
        # Convert the parser to a dictionary of dictionaries
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result