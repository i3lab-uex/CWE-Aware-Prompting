import json
import configparser
from typing import Any, Dict


def securely_load_data(byte_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize binary data safely using only approved formats.

    Parameters
    ----------
    byte_data : bytes
        Serialized data received in binary form.
    serialization_format : str
        One of the supported formats: 'json', 'ini'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the format is not among the allowed list or deserialization fails.
    """
    # List of allowed formats
    ALLOWED_FORMATS = {"json", "ini"}

    if serialization_format not in ALLOWED_FORMATS:
        raise ValueError(
            f"Format '{serialization_format}' is not supported or allowed."
        )

    try:
        # Convert bytes to text using UTF‑8. Any decoding error is treated as failure.
        text = byte_data.decode("utf-8")
    except Exception as exc:
        raise ValueError(f"Failed to decode bytes: {exc}") from exc

    if serialization_format == "json":
        try:
            return json.loads(text)
        except Exception as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    # serialization_format == "ini"
    config = configparser.ConfigParser()
    try:
        # ConfigParser expects a file-like object; read_string works with the text.
        config.read_string(text)
    except Exception as exc:
        raise ValueError(f"INI deserialization error: {exc}") from exc

    # Convert the ConfigParser to a plain dict for easier consumption.
    result: Dict[str, Dict[str, str]] = {
        section: dict(config[section]) for section in config.sections()
    }
    return result