import json
from typing import Any

def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data.
    data_format : str
        Format of the serialized data. Supported values: 'json'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the data_format is unsupported or considered insecure.
    """
    # Normalize format string to lower case
    fmt = data_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF-8, then parse JSON
            text = byte_stream.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte stream is not valid UTF-8 encoded JSON") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # Add more safe formats here if needed (e.g., 'yaml' with yaml.safe_load)
    # For now, only JSON is supported.

    raise ValueError(f"Unsupported or insecure format: '{data_format}'")