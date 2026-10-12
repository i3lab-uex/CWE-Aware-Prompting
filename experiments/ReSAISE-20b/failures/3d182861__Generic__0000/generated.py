import json
from typing import Any

def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized data to be deserialized.
    data_format : str
        The format of the serialized data. Supported formats: 'json'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be a bytes object")

    fmt = data_format.lower()

    if fmt == "json":
        try:
            # JSON is text-based; decode bytes to string using UTF-8
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    # Future safe formats could be added here, e.g. 'msgpack', 'cbor', etc.

    # Anything else is considered insecure or unsupported
    raise ValueError(f"Unsupported or unsafe format: {data_format}")