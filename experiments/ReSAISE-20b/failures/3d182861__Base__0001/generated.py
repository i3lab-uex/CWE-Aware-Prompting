import json
from typing import Any

def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `data` according to the specified `data_format`.

    Only a whitelist of formats is allowed. Unsupported or insecure
    formats raise ValueError.

    Parameters
    ----------
    data : bytes
        Serialized byte stream.
    data_format : str
        The format of the serialized data. Supported values are:
        - 'json'   : JSON encoded bytes.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Whitelist of safe formats
    SAFE_FORMATS = {
        'json': _deserialize_json,
    }

    # Normalize format string
    fmt = data_format.lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure data format: {data_format!r}")

    # Delegate to the appropriate deserializer
    return SAFE_FORMATS[fmt](data)


def _deserialize_json(data: bytes) -> Any:
    """
    Deserialize JSON data from a byte string.

    Parameters
    ----------
    data : bytes

    Returns
    -------
    Any
        Python representation of the JSON payload.
    """
    try:
        # Decode using UTF-8 (JSON is text-based)
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8 encoded JSON") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON payload") from exc