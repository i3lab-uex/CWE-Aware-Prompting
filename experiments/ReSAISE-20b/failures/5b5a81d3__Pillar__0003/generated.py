import json
import configparser
from io import BytesIO

def deserialize_payload(byte_sequence: bytes, data_format: str):
    """
    Deserialize binary payloads from trusted formats only.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized data in binary form.
    data_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    object
        The Python representation of the payload.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested.
    """
    if not isinstance(byte_sequence, (bytes, bytearray)):
        raise TypeError("byte_sequence must be bytes or bytearray")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            return json.loads(byte_sequence.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON payload") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use BytesIO
        try:
            parser.read_file(BytesIO(byte_sequence))
        except configparser.Error as exc:
            raise ValueError("Invalid INI payload") from exc
        # Convert to a nested dict for easier consumption
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result

    # Explicitly forbid pickle, marshal, yaml, etc.
    raise ValueError(f"Unsupported or unsafe format: {data_format}")