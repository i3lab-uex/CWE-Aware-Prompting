import json
import configparser
from io import StringIO

def safely_deserialize_data(serialized_bytes: bytes, method_format: str):
    """
    Deserialize binary data that was serialized using a permitted format.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary payload received from an external source.
    method_format : str
        The serialization mechanism used. Supported values are:
            - 'json'  : JSON format (text based).
            - 'ini'   : INI configuration format.

    Returns
    -------
    object
        The Python representation of the data (e.g. dict, list).

    Raises
    ------
    ValueError
        If the format is unsupported or not in the allowed list.
    json.JSONDecodeError, configparser.Error
        If the data cannot be parsed using the selected format.
    """
    # Only allow these formats to avoid unsafe deserialization (e.g., pickle).
    ALLOWED_FORMATS = {"json", "ini"}

    if method_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed format: {method_format!r}")

    # Decode bytes to text for parsing
    try:
        text = serialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8") from exc

    if method_format.lower() == "json":
        # json.loads is safe for simple data types
        return json.loads(text)

    if method_format.lower() == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object
        parser.read_file(StringIO(text))
        result = {}
        for section in parser.sections():
            # Convert each section to a dict of options
            result[section] = {k: v for k, v in parser.items(section)}
        return result

    # The above guard should make this unreachable
    raise ValueError(f"Unhandled format: {method_format!r}")