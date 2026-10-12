import json
from configparser import ConfigParser, ExtendedInterpolationError

def deserialize_payload(byte_sequence: bytes, data_format: str):
    """
    Safely deserialize binary data from trusted formats only.

    Parameters
    ----------
    byte_sequence : bytes
        The serialized payload.
    data_format : str
        The format used for deserialization. Supported values are:
        - 'json'
        - 'ini'

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or deserialization fails.
    """
    if not isinstance(byte_sequence, (bytes, bytearray)):
        raise TypeError("byte_sequence must be bytes or bytearray")

    fmt = data_format.lower()

    if fmt == "json":
        try:
            # Decode using UTF-8; raise ValueError on decode errors
            text = byte_sequence.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON payload") from exc

    if fmt == "ini":
        # ConfigParser expects a file-like object; we use StringIO
        try:
            text = byte_sequence.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for INI") from exc

        parser = ConfigParser(interpolation=ExtendedInterpolation())
        try:
            parser.read_string(text)
        except (ExtendedInterpolationError, ValueError) as exc:
            raise ValueError("Malformed INI payload") from exc

        # Convert to a plain dictionary: {section: {option: value}}
        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # If we reach here, the format is not supported
    raise ValueError(f"Unsupported deserialization format: {data_format}")