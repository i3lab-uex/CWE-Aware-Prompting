import json
import configparser
from io import BytesIO

# Allowed formats for deserialization
ALLOWED_FORMATS = {
    "json": json.loads,
    "ini": None,  # handled separately
}

def safely_deserialize_data(serialized_bytes: bytes, method_format: str):
    """
    Deserialize binary data safely based on a controlled set of formats.

    Parameters
    ----------
    serialized_bytes : bytes
        Binary data received from an external source.
    method_format : str
        The serialization format used: 'json' or 'ini'.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or not allowed.
    """
    if method_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization format: {method_format}")

    if method_format.lower() == "json":
        # JSON deserialization is safe for basic data structures
        try:
            text = serialized_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF-8 data for JSON deserialization") from exc
        return json.loads(text)

    if method_format.lower() == "ini":
        # configparser reads from a file-like object
        parser = configparser.ConfigParser()
        try:
            with BytesIO(serialized_bytes) as fp:
                parser.read_file(fp)
        except configparser.Error as exc:
            raise ValueError("Failed to parse INI data") from exc
        # Convert the parser into a regular dict for easier use
        return {section: dict(parser[section]) for section in parser.sections()}

    # Should never reach here because of the allowed formats check
    raise ValueError(f"Unhandled format: {method_format}")