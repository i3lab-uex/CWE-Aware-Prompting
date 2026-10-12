import json
from configparser import ConfigParser, NoSectionError, NoOptionError
from io import BytesIO

# Define the set of safe formats that are allowed for deserialization.
ALLOWED_FORMATS = {"json", "ini"}


def load_serialized_content(serialized_input: bytes, serialization_format: str):
    """
    Deserialize binary data from a trusted source.

    Parameters
    ----------
    serialized_input : bytes
        Binary representation of the data.
    serialization_format : str
        Format used for deserialization. Only ``json`` and ``ini`` are allowed.

    Returns
    -------
    object
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format is not recognized or deemed unsafe.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    if fmt == "json":
        # json.loads expects a string, so decode the bytes using UTF-8.
        try:
            text = serialized_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        return json.loads(text)

    if fmt == "ini":
        parser = ConfigParser()
        try:
            # configparser expects a file-like object. Use BytesIO to wrap the bytes.
            parser.read_file(BytesIO(serialized_input))
        except Exception as exc:
            raise ValueError("Failed to parse INI data") from exc

        # Convert the parsed config into a nested dictionary.
        result = {}
        for section in parser.sections():
            items = dict(parser.items(section))
            result[section] = items
        return result

    # This point should never be reached due to the earlier check, but keep it for safety.
    raise ValueError(f"Unhandled format: {serialization_format!r}")