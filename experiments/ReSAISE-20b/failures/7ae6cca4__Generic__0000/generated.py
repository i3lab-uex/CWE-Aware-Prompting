import json
import configparser
from typing import Any

# List of trusted formats that are considered safe for deserialization.
TRUSTED_FORMATS = {"json", "ini"}

def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data based on a trusted format identifier.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary form.
    format_string : str
        Identifier of the serialization format (e.g. 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or untrusted.
    """
    fmt = format_string.strip().lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Convert bytes to text safely; use UTF‑8 with replacement for invalid sequences.
    try:
        text = data_bytes.decode("utf-8", errors="replace")
    except Exception as exc:
        raise ValueError(f"Failed to decode bytes: {exc}") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # read_string expects a string with sections.
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError(f"Invalid INI data: {exc}") from exc

        # Convert the ConfigParser object to a plain dictionary.
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result

    # This point should never be reached because of the format check above.
    raise ValueError(f"Unhandled format: {format_string!r}")