import json
from configparser import ConfigParser
from io import BytesIO

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data into a Python object using only safe formats.

    Parameters
    ----------
    raw_bytes : bytes
        The binary data to deserialize.
    format_hint : str
        Hint indicating the serialization format. Supported values are
        'json' and 'ini'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_hint is not supported or considered unsafe.
    """
    fmt = format_hint.lower()

    if fmt == "json":
        try:
            # json.loads expects a string, so decode assuming UTF-8.
            return json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "ini":
        parser = ConfigParser()
        try:
            # configparser requires a file-like object
            parser.read_file(BytesIO(raw_bytes))
        except Exception as exc:
            raise ValueError(f"Invalid INI data: {exc}") from exc

        # Convert the ConfigParser object to a plain dict
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Any other format is considered unsafe or unsupported.
    raise ValueError(f"Unsupported or unsafe serialization format: {format_hint}")