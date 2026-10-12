import json
from typing import Any

def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only secure, predefined formats.

    Parameters
    ----------
    byte_stream : bytes
        Serialized data received from an external source.
    data_format : str
        The format of the serialized data. Supported values are:
            - 'json'   : JSON encoded data.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_format` is not one of the supported, secure formats.
    """
    # Normalize format string
    fmt = data_format.strip().lower()

    if fmt == "json":
        # Decode bytes to string using UTF-8; errors='strict' ensures invalid data raises an exception.
        try:
            text = byte_stream.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ValueError("Byte stream is not valid UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # If we reach this point, the format is unsupported.
    raise ValueError(f"Unsupported or insecure data format: {data_format}")