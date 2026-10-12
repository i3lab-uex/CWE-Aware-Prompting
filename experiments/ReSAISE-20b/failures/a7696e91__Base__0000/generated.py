import json
import configparser
from io import BytesIO
from typing import Any

# List of formats that are considered safe for deserialization.
_SAFE_FORMATS = {"json", "ini"}


def load_serialized_content(serialized_input: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data from an untrusted source using only a safe set of formats.

    Parameters
    ----------
    serialized_input : bytes
        The binary data to deserialize.
    serialization_format : str
        The format of the serialized data (e.g., 'json', 'ini').

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the requested format is not supported or deemed unsafe.
    json.JSONDecodeError, configparser.Error
        If the data cannot be parsed in the specified format.
    """
    # Normalise format name to lowercase for comparison
    fmt = serialization_format.lower()

    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    if fmt == "json":
        # JSON expects text; decode using UTF-8 (the standard encoding for JSON)
        try:
            text = serialized_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be UTF‑8 encoded") from exc
        return json.loads(text)

    if fmt == "ini":
        # configparser reads from a file-like object; use BytesIO to provide one
        parser = configparser.ConfigParser()
        try:
            with BytesIO(serialized_input) as fp:
                parser.read_file(fp)
        except configparser.Error as exc:
            raise ValueError("Failed to parse INI data") from exc
        # Convert the ConfigParser object into a nested dictionary for easier use.
        return {section: dict(parser.items(section)) for section in parser.sections()}

    # In practice, the code will never reach this point because of the earlier check,
    # but it is kept for completeness.
    raise ValueError(f"Unhandled format: {serialization_format!r}")