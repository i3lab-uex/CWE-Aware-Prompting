import json
import configparser
from io import BytesIO

__SAFE_FORMATS = {"json", "ini"}


def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data into a Python object using only safe formats.

    Parameters
    ----------
    raw_bytes : bytes
        The serialized data in binary form.
    format_hint : str
        A hint describing the serialization format ('json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format_hint is not supported or unsafe.
    """
    fmt = format_hint.lower()
    if fmt not in __SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_hint!r}")

    if fmt == "json":
        try:
            # Decode as UTF-8; errors replaced to avoid crashes on bad data
            text = raw_bytes.decode("utf-8", errors="replace")
            return json.loads(text)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON data: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            with BytesIO(raw_bytes) as f:
                parser.read_file(f)
        except configparser.Error as exc:
            raise ValueError(f"Failed to parse INI data: {exc}") from exc

        # Convert parser object into a nested dict
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point should never be reached due to the format check above
    raise ValueError(f"Unhandled format: {format_hint!r}")