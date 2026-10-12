import json
from configparser import ConfigParser, Error as ConfigError
from io import BytesIO

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data from a trusted source.

    Parameters
    ----------
    raw_bytes : bytes
        The serialized data.
    format_hint : str
        One of 'json' or 'ini'. Other values raise an exception.

    Returns
    -------
    object
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise ValueError("Input must be bytes-like.")

    fmt = format_hint.lower()
    if fmt == "json":
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF-8 encoded.") from exc
        return json.loads(text)

    if fmt == "ini":
        parser = ConfigParser()
        try:
            # ConfigParser expects a file-like object; use BytesIO
            parser.read_file(BytesIO(raw_bytes))
        except ConfigError as exc:
            raise ValueError("Invalid INI format.") from exc
        # Convert to a plain dictionary for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    raise ValueError(f"Unsupported or unsafe format: {format_hint!r}")