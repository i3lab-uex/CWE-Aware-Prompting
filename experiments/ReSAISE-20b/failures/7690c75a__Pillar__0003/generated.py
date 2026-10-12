import json
from typing import Any


def decode_data_stream(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object only if the format is explicitly allowed.

    Supported formats (case‑insensitive):
        - json

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        Identifier of the serialization format.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    # Normalise the format string for comparison
    fmt = data_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to string and parse JSON
            return json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc
    else:
        # Explicitly reject all other formats to avoid unsafe deserialization.
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")