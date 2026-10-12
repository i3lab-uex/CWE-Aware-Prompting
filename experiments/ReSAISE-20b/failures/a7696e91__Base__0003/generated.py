import json
import configparser
from typing import Any

def load_serialized_content(
    serialized_input: bytes,
    serialization_format: str
) -> Any:
    """
    Deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    serialized_input : bytes
        The binary data to deserialize.
    serialization_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or deserialization fails.
    """
    if not isinstance(serialized_input, bytes):
        raise TypeError("serialized_input must be of type 'bytes'")

    fmt = serialization_format.lower()

    if fmt == "json":
        try:
            # json.loads expects a str, so decode using UTF‑8.
            text = serialized_input.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF‑8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file‑like object with text.
            parser.read_file(io.StringIO(serialized_input.decode("utf-8")))
        except (UnicodeDecodeError, configparser.Error) as exc:
            raise ValueError("Invalid INI data") from exc
        # Convert the parser to a nested dict for easier consumption.
        result = {section: dict(parser[section]) for section in parser.sections()}
        return result

    else:
        raise ValueError(f"Unsupported serialization format: {serialization_format!r}")