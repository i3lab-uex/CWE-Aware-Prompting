import json
from configparser import ConfigParser
from io import BytesIO

# Safe formats that are allowed for deserialization.
SAFE_FORMATS = {"json", "ini"}

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Deserialize binary data safely using only permitted formats.

    Parameters
    ----------
    data_input : bytes
        Serialized binary data received from an external source.
    format_type : str
        The serialization mechanism used ('json' or 'ini').

    Returns
    -------
    Any
        The Python object produced by deserialization.

    Raises
    ------
    ValueError
        If the format_type is not in the list of safe formats.
    """
    fmt = format_type.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Deserialization format '{format_type}' is not allowed.")

    if fmt == "json":
        # Decode bytes to string and parse JSON.
        try:
            return json.loads(data_input.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        # Parse INI data into a dictionary of sections.
        parser = ConfigParser()
        try:
            # ConfigParser expects a file-like object; BytesIO provides that.
            parser.read_file(BytesIO(data_input))
        except Exception as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the parsed configuration into a plain dictionary.
        config_dict = {}
        for section in parser.sections():
            config_dict[section] = dict(parser.items(section))
        return config_dict

    # The code should never reach here because of the SAFE_FORMATS check.
    raise ValueError(f"Unhandled format: {format_type}")