import json
import configparser
from typing import Any, Dict


def deserialize_payload(byte_sequence: bytes, data_format: str) -> Any:
    """
    Deserialize binary payloads from trusted formats only.

    Parameters
    ----------
    byte_sequence : bytes
        The binary data to be deserialized.
    data_format : str
        The format of the payload. Supported values are:
            - 'json'
            - 'ini'

    Returns
    -------
    Any
        The deserialized Python object. For JSON it returns the parsed
        structure (dict, list, etc.). For INI it returns a nested dict
        of sections and options.

    Raises
    ------
    ValueError
        If `data_format` is not in the allowed set.
    json.JSONDecodeError
        If JSON decoding fails.
    """
    # Normalize format string
    fmt = data_format.strip().lower()

    if fmt == "json":
        # JSON is safe when decoded as UTF‑8
        text = byte_sequence.decode("utf-8")
        return json.loads(text)

    if fmt == "ini":
        # Parse INI safely into a dictionary
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a string, so decode UTF‑8
            parser.read_string(byte_sequence.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise ValueError("INI payload is not valid UTF‑8") from exc

        # Convert to a plain dict for easier use
        result: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # If we reach here, the format is unsupported
    raise ValueError(f"Unsupported or unsafe deserialization format: {data_format}")