import json
import configparser
from typing import Any, Dict

# Define the list of trusted formats
TRUSTED_FORMATS = {"json", "ini"}


def decode_serialized_data(data_bytes: bytes, format_string: str) -> Any:
    """
    Safely deserialize binary data based on a trusted format string.

    Parameters
    ----------
    data_bytes : bytes
        The incoming serialized data in binary format.
    format_string : str
        Identifier of the serialization format (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not in the list of trusted formats.
    """
    fmt = format_string.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or untrusted format: {format_string!r}")

    # Decode bytes to text safely
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"Unable to decode bytes as UTF-8: {exc}") from exc

    if fmt == "json":
        # json.loads can raise JSONDecodeError
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # configparser expects a file-like object; use read_string
        parser.read_string(text)
        # Convert to nested dict: section -> dict of options
        result: Dict[str, Dict[str, str]] = {
            section: dict(parser.items(section)) for section in parser.sections()
        }
        return result

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_string!r}")