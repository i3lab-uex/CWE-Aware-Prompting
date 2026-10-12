import json
import configparser
from io import BytesIO

# List of safe, supported serialization formats
SAFE_FORMATS = {"json", "ini"}

def load_serialized_content(serialized_input: bytes, serialization_format: str):
    """
    Deserialize binary data from a trusted source using only safe formats.

    Parameters
    ----------
    serialized_input : bytes
        The binary data to be deserialized.
    serialization_format : str
        The format of the serialized data ('json' or 'ini').

    Returns
    -------
    object
        The Python representation of the serialized data.

    Raises
    ------
    ValueError
        If the format is not in SAFE_FORMATS or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    if fmt == "json":
        try:
            text = serialized_input.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

    if fmt == "ini":
        try:
            parser = configparser.ConfigParser()
            # ConfigParser expects a file-like object; BytesIO provides that
            parser.read_file(BytesIO(serialized_input))
            # Convert to a plain dictionary for easier consumption
            return {section: dict(parser.items(section)) for section in parser.sections()}
        except Exception as exc:
            raise ValueError(f"Failed to deserialize INI: {exc}") from exc