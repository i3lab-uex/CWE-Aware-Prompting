import json
import configparser
from io import BytesIO

# List of formats considered safe for deserialization
_SAFE_FORMATS = {"json", "ini"}

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data into a Python object using only safe formats.

    Parameters
    ----------
    raw_bytes : bytes
        The binary data to deserialize.
    format_hint : str
        The format of the serialized data. Supported values are
        'json' and 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_hint is unsupported or considered unsafe.
    """
    fmt = format_hint.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_hint!r}")

    if fmt == "json":
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("JSON decoding failed") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file‑like object; BytesIO provides that
            parser.read_file(BytesIO(raw_bytes))
        except configparser.Error as exc:
            raise ValueError("INI parsing failed") from exc

        # Convert the parsed data into a plain dict
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # This point should never be reached due to the guard above
    raise ValueError(f"Unhandled format: {format_hint!r}")