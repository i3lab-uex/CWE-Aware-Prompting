import json
from typing import Any


def bytes_to_obj(data_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize raw bytes into a Python object using only trusted formats.

    Parameters
    ----------
    data_bytes : bytes
        Serialized representation of the object.
    format_name : str
        The serialization format. Supported formats are:
            - 'json'  (default, safe for untrusted data)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is unsupported or considered unsafe.
    """
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise TypeError("data_bytes must be a bytes-like object")

    fmt = format_name.lower()
    if fmt == "json":
        # Decode bytes to str using UTF-8 (common default for JSON)
        text = data_bytes.decode("utf-8")
        return json.loads(text)

    # If you want to add more safe formats, do so here
    raise ValueError(f"Unsupported or unsafe format: {format_name}")