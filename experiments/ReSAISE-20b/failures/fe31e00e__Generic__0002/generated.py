import json
from configparser import ConfigParser
from io import StringIO
from typing import Any


# List of formats considered safe for deserialization
ALLOWED_FORMATS = {"json", "ini"}


def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data safely using only permitted formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary format.
    serialization_format : str
        The mechanism used to serialize the data ('json', 'ini').

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not allowed or unsupported.
    """
    if serialization_format.lower() not in ALLOWED_FORMATS:
        raise ValueError(
            f"Format '{serialization_format}' is not allowed or unsupported."
        )

    if serialization_format.lower() == "json":
        try:
            text = byte_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data.") from exc

    if serialization_format.lower() == "ini":
        try:
            text = byte_data.decode("utf-8")
            parser = ConfigParser()
            parser.read_file(StringIO(text))
            # Convert to a nested dictionary for easier consumption
            config_dict = {
                section: dict(parser.items(section)) for section in parser.sections()
            }
            return config_dict
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode INI data.") from exc
        except Exception as exc:  # pragma: no cover
            raise ValueError("Failed to parse INI data.") from exc