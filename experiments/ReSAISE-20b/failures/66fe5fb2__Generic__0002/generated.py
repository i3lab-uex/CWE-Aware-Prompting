import json
import configparser
from io import BytesIO, StringIO

# Define a whitelist of safe formats for deserialization
SAFE_FORMATS = {"json", "ini"}

def safely_deserialize_data(serialized_bytes: bytes, method_format: str):
    """
    Deserialize binary data safely using only whitelisted formats.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary data to deserialize.
    method_format : str
        The serialization format used (e.g., 'json', 'ini').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or unsupported.
    """
    fmt = method_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {method_format}")

    if fmt == "json":
        # json.loads expects a str, so decode using utf-8
        try:
            text = serialized_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF-8 data for JSON deserialization") from exc
        return json.loads(text)

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object with text
        try:
            stream = StringIO(serialized_bytes.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF-8 data for INI deserialization") from exc
        parser.read_file(stream)
        # Convert to a nested dictionary for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # The whitelist prevents reaching this point, but keep a defensive clause
    raise ValueError(f"Deserialization for format '{fmt}' is not implemented.")