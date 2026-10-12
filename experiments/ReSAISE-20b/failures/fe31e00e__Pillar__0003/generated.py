import json
import configparser
from io import BytesIO
from typing import Any


def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data in a controlled and safe manner.

    Parameters
    ----------
    byte_data : bytes
        The serialized data received in binary format.
    serialization_format : str
        The name of the serialization mechanism used. Only a limited set of formats
        is supported for security reasons.

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the requested format is not in the list of allowed formats.
    json.JSONDecodeError, configparser.Error
        If deserialization fails due to malformed input.
    """
    # Normalise format name
    fmt = serialization_format.lower()

    if fmt == "json":
        # JSON is safe to load as it only constructs basic data types
        return json.loads(byte_data.decode("utf-8"))

    if fmt == "ini":
        # INI files are parsed into a ConfigParser object
        parser = configparser.ConfigParser()
        # ConfigParser expects a file-like object; use BytesIO
        with BytesIO(byte_data) as f:
            parser.read_file(f)
        # Convert the ConfigParser to a plain dict for easier consumption
        return {section: dict(parser[section]) for section in parser.sections()}

    # Add more safe formats here if desired

    raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")