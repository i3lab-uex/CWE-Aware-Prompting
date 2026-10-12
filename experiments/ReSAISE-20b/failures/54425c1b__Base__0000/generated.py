import json
import configparser
from io import BytesIO

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "ini"}

def deserialize_data_safely(data_input: bytes, format_type: str):
    """
    Safely deserialize binary data using only permitted formats.

    Parameters
    ----------
    data_input : bytes
        The serialized binary data.
    format_type : str
        The serialization mechanism used ('json', 'ini').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or not allowed.
    json.JSONDecodeError
        For malformed JSON input.
    configparser.Error
        For malformed INI input.
    """
    # Normalise format_type to lowercase for comparison
    fmt = format_type.strip().lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Format '{format_type}' is not allowed for deserialization.")

    # Ensure the data is decoded as UTF‑8 text before parsing
    try:
        text = data_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8 encoded text.") from exc

    if fmt == "json":
        # json.loads is safe for untrusted data; it only constructs basic types
        return json.loads(text)

    if fmt == "ini":
        # Parse INI into a nested dictionary
        parser = configparser.ConfigParser()
        parser.read_file(BytesIO(text.encode("utf-8")))
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # In theory we should never reach this point because of the SAFE_FORMATS check
    raise ValueError(f"Unhandled format: {format_type}")