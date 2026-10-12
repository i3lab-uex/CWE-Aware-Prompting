import json
import configparser
from io import BytesIO


def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data coming from an untrusted source.

    Supported formats (safe only):
        - 'json': JSON text
        - 'ini' : INI configuration

    Parameters
    ----------
    raw_bytes : bytes
        The binary representation of the data.
    format_hint : str
        A string indicating which format to use for deserialization.

    Returns
    -------
    Any
        The Python object resulting from the deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise TypeError("raw_bytes must be bytes or bytearray")

    fmt = format_hint.lower()

    if fmt == "json":
        # JSON is safe; json.loads will only produce basic Python objects
        try:
            return json.loads(raw_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        # configparser parses INI files into a dictionary-like structure
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use BytesIO
            parser.read_file(BytesIO(raw_bytes))
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert to a plain dict for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # Pickle and other formats are explicitly disallowed to avoid
    # executing arbitrary code from untrusted sources.
    raise ValueError(f"Unsupported or unsafe format: {format_hint}")