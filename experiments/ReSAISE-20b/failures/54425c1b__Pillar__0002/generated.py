import json
import configparser
from io import StringIO

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Deserialize binary data safely based on the specified format.

    Supported formats:
        - 'json': JSON encoded bytes
        - 'ini' : INI style configuration (returns a nested dict)

    Any other format will raise a ValueError.

    Parameters
    ----------
    data_input : bytes
        Serialized binary data.
    format_type : str
        Identifier of the serialization format.

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format_type is not in the allowed list.
    json.JSONDecodeError
        If JSON decoding fails.
    configparser.Error
        If INI parsing fails.
    """
    allowed_formats = {'json', 'ini'}

    if format_type not in allowed_formats:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}")

    # Ensure we operate on a string for text-based formats
    try:
        data_str = data_input.decode('utf-8')
    except Exception as exc:  # pragma: no cover
        raise ValueError("Input data must be valid UTF-8 bytes") from exc

    if format_type == 'json':
        # JSON is safe as it only builds basic Python data structures
        return json.loads(data_str)

    if format_type == 'ini':
        # Parse INI into a nested dictionary
        parser = configparser.ConfigParser()
        try:
            parser.read_file(StringIO(data_str))
        except Exception as exc:  # pragma: no cover
            raise configparser.Error("INI parsing failed") from exc

        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point is unreachable due to the allowed_formats check
    raise ValueError(f"Unhandled format: {format_type!r}")