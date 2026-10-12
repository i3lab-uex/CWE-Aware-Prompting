import json
import configparser
from io import StringIO

# A whitelist of safe serialization formats.
SAFE_FORMATS = {
    "json",
    "ini",
}

def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Deserialize binary data safely based on a whitelisted format.

    Parameters
    ----------
    byte_data : bytes
        The serialized data received in binary form.
    serialization_format : str
        Identifier of the format used to serialize the data (e.g., 'json', 'ini').

    Returns
    -------
    object
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Deserialization format '{serialization_format}' is not allowed.")

    try:
        if fmt == "json":
            # json.loads expects a str, so decode bytes safely
            return json.loads(byte_data.decode("utf-8"))
        elif fmt == "ini":
            # ConfigParser reads from a file-like object; use StringIO
            parser = configparser.ConfigParser()
            parser.read_file(StringIO(byte_data.decode("utf-8")))
            # Convert the parsed data into a plain dict for easier consumption
            return {section: dict(parser[section]) for section in parser.sections()}
    except Exception as exc:
        # Wrap any exception to avoid leaking internal details
        raise ValueError(f"Failed to deserialize data: {exc}") from None

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     json_bytes = b'{"key": "value"}'
#     print(securely_load_data(json_bytes, 'json'))
#     ini_bytes = b'[section]\nkey=value\n'
#     print(securely_load_data(ini_bytes, 'ini'))