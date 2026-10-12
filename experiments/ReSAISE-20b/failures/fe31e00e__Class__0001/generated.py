import json
import configparser
from io import BytesIO

# List of formats considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}


def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Safely deserialize binary data according to a restricted set of formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary format.
    serialization_format : str
        The name of the serialization mechanism used ('json' or 'ini').

    Returns
    -------
    object
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {serialization_format}")

    if fmt == "json":
        try:
            # json.loads accepts str, so decode using UTF-8 safely
            return json.loads(byte_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use BytesIO
            parser.read_file(BytesIO(byte_data))
        except configparser.Error as exc:
            raise ValueError("Failed to deserialize INI data") from exc

        # Convert ConfigParser object to a plain dictionary
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result

    # This point should never be reached due to the ALLOWED_FORMATS check
    raise ValueError(f"Unhandled format: {serialization_format}")