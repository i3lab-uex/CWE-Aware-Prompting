import json
from configparser import ConfigParser, Error as ConfigError

# List of safe formats that are allowed for deserialization
SAFE_FORMATS = {"json", "ini"}

def convert_serialized_data(raw_bytes: bytes, format_hint: str):
    """
    Deserialize binary data that comes from an external source.

    Parameters
    ----------
    raw_bytes : bytes
        The serialized data in binary form.
    format_hint : str
        One of the supported formats ('json', 'ini').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = format_hint.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {format_hint}")

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = ConfigParser()
        try:
            # read_string expects a str, not bytes
            parser.read_string(text)
        except ConfigError as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the ConfigParser to a plain dict
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # This point should never be reached due to the earlier guard
    raise ValueError(f"Unhandled format: {format_hint}")