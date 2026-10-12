import json
from configparser import ConfigParser, NoSectionError
from io import BytesIO

def load_serialized_content(serialized_input: bytes, serialization_format: str):
    """
    Deserialize binary data from trusted formats only.

    Parameters
    ----------
    serialized_input : bytes
        Binary data to be deserialized.
    serialization_format : str
        Format of the serialized data. Only 'json' and 'ini'
        are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not recognized or deemed unsafe.
    """
    fmt = serialization_format.lower()

    if fmt == 'json':
        try:
            text = serialized_input.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF‑8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == 'ini':
        parser = ConfigParser()
        try:
            # configparser expects a file-like object
            parser.read_file(BytesIO(serialized_input))
        except Exception as exc:
            raise ValueError("Invalid INI data") from exc

        config_dict = {}
        for section in parser.sections():
            config_dict[section] = dict(parser.items(section))
        return config_dict

    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")