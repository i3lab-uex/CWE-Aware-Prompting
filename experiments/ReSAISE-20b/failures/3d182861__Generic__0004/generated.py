import json
from typing import Any


def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized data that needs to be deserialized.
    data_format : str
        The format of the serialized data. Supported values are:
            - 'json'   : Standard JSON decoding.
        Any other value will raise a ValueError.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If `data_format` is unsupported or considered insecure.
    """
    if not isinstance(data, bytes):
        raise TypeError("data must be of type 'bytes'")

    fmt = data_format.lower()
    if fmt == "json":
        try:
            # JSON expects text; decode bytes using UTF-8
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc
    else:
        # Reject all other formats to avoid unsafe deserialization
        raise ValueError(f"Unsupported or insecure data format: {data_format}")