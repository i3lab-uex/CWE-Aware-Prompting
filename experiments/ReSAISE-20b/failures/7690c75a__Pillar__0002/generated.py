import json
from typing import Any


def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object for a limited set of safe formats.

    Parameters
    ----------
    data : bytes
        The serialized stream of data.
    data_format : str
        Format specifier for the data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested.
    """
    # Define the set of allowed formats. Only JSON is considered safe for arbitrary data.
    _ALLOWED_FORMATS = {"json"}

    # Normalise format string to lower case for comparison
    fmt = data_format.strip().lower()

    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    # At this point we only support JSON.
    try:
        # Decode bytes to UTF-8 string safely. Invalid UTF-8 will raise UnicodeDecodeError.
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

    try:
        # json.loads automatically handles nested structures safely.
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc