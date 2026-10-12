import json
import configparser
from typing import Any, Dict

def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Safely deserialize binary data based on the specified format.

    Parameters
    ----------
    data_input : bytes
        Serialized data received in binary form.
    format_type : str
        The serialization mechanism used. Supported values are:
        - 'json'   : JSON format (text based).
        - 'ini'    : INI/ConfigParser format.

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format_type is not supported or considered unsafe.
    """
    # Ensure we have bytes input
    if not isinstance(data_input, (bytes, bytearray)):
        raise TypeError("data_input must be bytes-like")

    # Decode the binary data into a string
    try:
        text = data_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("data_input is not valid UTF‑8") from exc

    # Define safe deserialization handlers
    def _load_json(s: str) -> Any:
        return json.loads(s)

    def _load_ini(s: str) -> Dict[str, Dict[str, str]]:
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use read_string
        parser.read_string(s)
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    handlers = {
        "json": _load_json,
        "ini":  _load_ini,
    }

    # Lookup the handler
    handler = handlers.get(format_type.lower())
    if handler is None:
        raise ValueError(f"Unsupported or unsafe format: {format_type!r}")

    # Perform deserialization
    return handler(text)