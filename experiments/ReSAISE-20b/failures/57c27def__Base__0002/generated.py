import json
from configparser import ConfigParser
from io import BytesIO

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Safely deserialize binary data that comes from an external source.

    Parameters
    ----------
    raw_bytes : bytes
        Binary data to be deserialized.
    format_hint : str
        One of the supported formats: 'json' or 'ini'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_hint is unsupported or unsafe.
    """
    # Normalise the hint to lower‑case
    fmt = format_hint.lower()

    if fmt == "json":
        # json is safe for deserialization of basic data types
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        return json.loads(text)

    if fmt == "ini":
        # Use configparser which only parses configuration data
        parser = ConfigParser()
        try:
            with BytesIO(raw_bytes) as f:
                parser.read_file(f)
        except Exception as exc:  # pragma: no cover
            raise ValueError("Invalid INI data") from exc

        # Convert the parsed structure into a plain dict
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # All other formats are considered unsafe or unsupported
    raise ValueError(f"Unsupported format: {format_hint}")