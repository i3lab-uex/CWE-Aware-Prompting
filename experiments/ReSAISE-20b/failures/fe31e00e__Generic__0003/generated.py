import json
from configparser import ConfigParser
from io import StringIO


def securely_load_data(byte_data: bytes, serialization_format: str):
    """
    Deserialize binary data using only a safe set of formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary format.
    serialization_format : str
        The name of the serialization mechanism used.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not allowed or unsupported.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    fmt = serialization_format.lower()
    if fmt == "json":
        # JSON is safe for deserialization
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

    if fmt == "ini":
        # INI is also safe; we parse into a dictionary of sections
        try:
            text = byte_data.decode("utf-8")
            parser = ConfigParser()
            # read_string expects a file-like object; use StringIO
            parser.read_file(StringIO(text))
        except UnicodeDecodeError as exc:
            raise ValueError(f"Failed to decode INI data: {exc}") from exc

        result = {}
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    # Reject any other format
    raise ValueError(f"Deserialization format '{serialization_format}' is not allowed.")