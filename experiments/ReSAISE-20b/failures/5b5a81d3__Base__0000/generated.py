import json
import configparser
from typing import Any, Dict

def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to deserialize.
    data_format : str
        The format identifier. Only 'json' and 'ini' are supported.

    Returns
    -------
    Any
        The deserialized Python object. For 'json' this is the result of json.loads.
        For 'ini' this is a dictionary mapping section names to dictionaries of key/value pairs.

    Raises
    ------
    ValueError
        If the data_format is not recognized or considered unsafe.
    """
    format_lower = data_format.lower()

    if format_lower == "json":
        try:
            text = byte_sequence.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON payload must be UTF-8 encoded") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if format_lower == "ini":
        config = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use BytesIO
            from io import StringIO
            text = byte_sequence.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("INI payload must be UTF-8 encoded") from exc

        try:
            config.read_string(text)
        except configparser.Error as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert ConfigParser to a plain dict for easier consumption
        result: Dict[str, Dict[str, str]] = {}
        for section in config.sections():
            result[section] = dict(config.items(section))
        return result

    raise ValueError(f"Unsupported or unsafe format: {data_format}")