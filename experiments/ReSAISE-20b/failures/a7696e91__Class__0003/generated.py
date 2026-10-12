import json
import configparser
from typing import Any


def load_serialized_content(
    serialized_input: bytes,
    serialization_format: str
) -> Any:
    """
    Deserialize binary data from a trusted format.

    Parameters
    ----------
    serialized_input : bytes
        The raw binary data to deserialize.
    serialization_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or deserialization fails.
    """
    if not isinstance(serialized_input, (bytes, bytearray)):
        raise TypeError("serialized_input must be bytes or bytearray")

    fmt = serialization_format.lower()

    # Decode the binary data to a text string
    try:
        text = serialized_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # read_string expects a file‑like string; it may raise
            # configparser.Error for malformed data.
            parser.read_string(text)
        except (configparser.Error, ValueError) as exc:
            raise ValueError("Invalid INI data") from exc

        # Convert the ConfigParser object to a plain dict for easier use
        result = {section: dict(parser.items(section)) for section in parser.sections()}
        return result

    raise ValueError(f"Unsupported serialization format: {serialization_format}")