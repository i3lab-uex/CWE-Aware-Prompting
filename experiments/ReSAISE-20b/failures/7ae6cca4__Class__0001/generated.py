import json
import configparser
from io import BytesIO

# Allowed formats that are considered safe for deserialization
ALLOWED_FORMATS = {"json", "ini"}

def decode_serialized_data(data_bytes: bytes, format_string: str):
    """
    Deserialize `data_bytes` according to the trusted `format_string`.

    Parameters
    ----------
    data_bytes : bytes
        The binary payload to deserialize.
    format_string : str
        Identifier of the serialization format (e.g., 'json', 'ini').

    Returns
    -------
    object
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or untrusted.
    """
    fmt = format_string.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    if fmt == "json":
        # json.loads expects a str, not bytes
        try:
            return json.loads(data_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object
            parser.read_file(BytesIO(data_bytes))
        except configparser.Error as exc:
            raise ValueError(f"Invalid INI data: {exc}") from exc
        # Convert to a simple dict for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # The following line is never reached due to the earlier check,
    # but it keeps type-checkers happy.
    raise ValueError(f"Unhandled format: {format_string!r}")