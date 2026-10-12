import json
import configparser
from typing import Any, Union

def load_serialized_content(serialized_input: bytes,
                            serialization_format: str) -> Any:
    """
    Deserialize binary data from a trusted set of formats.

    Parameters
    ----------
    serialized_input : bytes
        The binary data to deserialize.
    serialization_format : str
        One of the supported formats: 'json', or 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not supported or the data cannot be parsed.
    """
    if not isinstance(serialized_input, bytes):
        raise TypeError("serialized_input must be of type 'bytes'")

    fmt = serialization_format.lower()

    # Convert bytes to string safely
    try:
        text = serialized_input.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8") from exc

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("JSON deserialization failed") from exc

    if fmt == "ini":
        parser = configparser.ConfigParser()
        try:
            # ConfigParser expects a file-like object; use read_string
            parser.read_string(text)
        except configparser.Error as exc:
            raise ValueError("INI deserialization failed") from exc

        # Convert to a plain dictionary for easier use
        result: dict[str, dict[str, str]] = {
            section: dict(parser[section]) for section in parser.sections()
        }
        return result

    # Any other format is explicitly disallowed
    raise ValueError(f"Unsupported serialization format: {serialization_format}")