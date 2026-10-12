import json
import configparser
from io import StringIO
from typing import Any


# Controlled list of formats considered safe for deserialization.
SAFE_FORMATS = {
    "json": _deserialize_json,
    "ini": _deserialize_ini,
}


def safely_deserialize_data(serialized_bytes: bytes, method_format: str) -> Any:
    """
    Deserialize binary data that was serialized using a known, safe format.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary payload received from an external source.
    method_format : str
        Identifier of the serialization format used. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the safe list or if deserialization fails.
    """
    # Normalise method name to lower case to avoid accidental mismatches
    fmt = method_format.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(
            f"Deserialization format '{method_format}' is not allowed. "
            f"Allowed formats: {', '.join(SAFE_FORMATS.keys())}"
        )

    # Delegate to the appropriate deserializer
    return SAFE_FORMATS[fmt](serialized_bytes)


# --------------------------------------------------------------------------- #
# Internal helper functions for each supported format
# --------------------------------------------------------------------------- #

def _deserialize_json(data: bytes) -> Any:
    """
    Deserialize JSON data from bytes.
    Raises ValueError on decoding or parsing errors.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF‑8") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse JSON data") from exc


def _deserialize_ini(data: bytes) -> configparser.ConfigParser:
    """
    Deserialize INI data from bytes into a ConfigParser object.
    Raises ValueError on decoding or parsing errors.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("INI data is not valid UTF‑8") from exc

    parser = configparser.ConfigParser()
    try:
        # ConfigParser expects a file-like object; StringIO wraps the text.
        parser.read_file(StringIO(text))
    except configparser.Error as exc:
        raise ValueError("Failed to parse INI data") from exc

    return parser