import json
import configparser
from io import BytesIO
from typing import Any

class UnsupportedFormatError(RuntimeError):
    """Raised when the supplied format is not allowed for deserialization."""
    pass

def convert_serialized_data(raw_bytes: bytes, format_hint: str) -> Any:
    """
    Deserialize binary data that comes from external sources.

    Parameters
    ----------
    raw_bytes : bytes
        The binary payload to deserialize.
    format_hint : str
        The name of the serialization format. Supported values are:
        - 'json'   : safe JSON deserialization.
        - 'ini'    : configuration file format (INI), parsed into a dict.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    UnsupportedFormatError
        If `format_hint` is not in the whitelist of safe formats.
    ValueError
        If deserialization fails (e.g., malformed data).
    """
    # Whitelist of safe formats
    _SAFE_FORMATS = {"json", "ini"}

    fmt = format_hint.lower()
    if fmt not in _SAFE_FORMATS:
        raise UnsupportedFormatError(
            f"Unsupported or unsafe format requested: {format_hint!r}"
        )

    try:
        if fmt == "json":
            # Decode bytes to str using UTF-8; raise UnicodeDecodeError if invalid
            text = raw_bytes.decode("utf-8")
            return json.loads(text)

        if fmt == "ini":
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; BytesIO provides that
            parser.read_file(BytesIO(raw_bytes))
            # Convert the ConfigParser to a plain dict for easier consumption
            return {section: dict(parser[section]) for section in parser.sections()}

    except Exception as exc:
        # Re-raise with a clearer message
        raise ValueError(f"Failed to deserialize data as {format_hint!r}: {exc}") from exc