import json
import configparser
from io import BytesIO
from typing import Any, Dict

# Define the set of safe serialization formats
_SAFE_FORMATS = {"json", "ini"}

def load_serialized_content(
    serialized_input: bytes,
    serialization_format: str
) -> Any:
    """
    Deserialize binary data from a trusted format.

    Parameters
    ----------
    serialized_input : bytes
        The binary payload to deserialize.
    serialization_format : str
        One of the supported formats ('json', 'ini').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in _SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    if fmt == "json":
        try:
            # JSON expects text, so decode using UTF-8
            return json.loads(serialized_input.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; BytesIO works for binary data
            parser.read_file(BytesIO(serialized_input))
        except configparser.Error as exc:
            raise ValueError("Failed to deserialize INI data") from exc

        # Convert the parser's contents into a plain dictionary
        ini_dict: Dict[str, Dict[str, str]] = {}
        for section in parser.sections():
            ini_dict[section] = dict(parser.items(section))
        return ini_dict

    # The following line should never be reached due to the earlier check,
    # but it satisfies static type checkers.
    raise ValueError(f"Unhandled format: {serialization_format}")