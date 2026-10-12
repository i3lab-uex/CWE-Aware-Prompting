import json
from typing import Any


def security_content_deserializer(byte_stream: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object only for secure, predefined formats.

    Parameters
    ----------
    byte_stream : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data. Supported values are:
            - 'json'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Normalise and validate the requested format
    fmt = data_format.strip().lower()
    if fmt != 'json':
        raise ValueError(f"Unsupported or insecure data format: {data_format!r}")

    # Decode bytes to string and parse JSON safely
    try:
        text = byte_stream.decode('utf-8')
    except Exception as exc:  # pragma: no cover
        raise ValueError("Byte stream must be UTF-8 encoded JSON.") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:  # pragma: no cover
        raise ValueError("Invalid JSON data.") from exc