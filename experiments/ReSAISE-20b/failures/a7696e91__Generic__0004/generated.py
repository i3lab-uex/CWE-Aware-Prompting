import json
import configparser
import io
from typing import Any

# Allowed safe serialization formats
_SAFE_FORMATS = {"json", "ini"}


def load_serialized_content(serialized_input: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data from a trusted source.

    Parameters
    ----------
    serialized_input : bytes
        The raw binary data to deserialize.
    serialization_format : str
        Format identifier, e.g. 'json' or 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the list of safe formats.
    """
    fmt = serialization_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    if fmt == "json":
        # JSON expects text, so decode bytes first
        try:
            decoded = serialized_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        return json.loads(decoded)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use BytesIO
        try:
            parser.read_file(io.BytesIO(serialized_input))
        except configparser.Error as exc:
            raise ValueError("Malformed INI data") from exc

        # Convert the parser to a nested dictionary
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # The following line is unreachable due to the earlier check,
    # but keeps type-checkers happy.
    raise ValueError(f"Unhandled format: {serialization_format}")