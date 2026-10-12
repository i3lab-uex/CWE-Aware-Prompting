import json
import configparser
from typing import Any

# Define the set of formats that are allowed to be deserialized.
ALLOWED_FORMATS = {"json", "ini"}

def deserialize_data_safely(data_input: bytes, format_type: str) -> Any:
    """
    Deserialize binary data safely using only permitted formats.

    Parameters
    ----------
    data_input : bytes
        The serialized binary payload.
    format_type : str
        Identifier of the serialization mechanism ('json', 'ini').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format_type is not in the allowed list.
    json.JSONDecodeError, configparser.Error
        If deserialization fails for the chosen format.
    """
    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {format_type!r}")

    if fmt == "json":
        # JSON is safe for basic data types.
        return json.loads(data_input.decode("utf-8"))

    if fmt == "ini":
        # ConfigParser reads INI files into a dictionary-like structure.
        parser = configparser.ConfigParser()
        # ConfigParser expects text input; decode bytes accordingly.
        parser.read_string(data_input.decode("utf-8"))
        # Convert the parsed data into a nested dict.
        return {section: dict(parser[section]) for section in parser.sections()}

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled format: {format_type!r}")