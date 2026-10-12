import json
import configparser
from io import StringIO
from typing import Any


# A whitelist of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json", "ini"}


def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data based on a trusted format identifier.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary format.
    format_string : str
        Identifier of the serialization format (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    fmt = format_string.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Convert bytes to text; assume UTF-8 encoding.  If decoding fails,
    # we raise a ValueError rather than silently swallowing the error.
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Data is not valid UTF-8: {exc}") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use StringIO.
            parser.read_file(StringIO(text))
        except configparser.Error as exc:
            raise ValueError(f"INI deserialization error: {exc}") from exc

        # Convert the parsed structure into a plain dictionary.
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # The code should never reach this point due to the whitelist check.
    raise ValueError(f"Unhandled format: {format_string!r}")