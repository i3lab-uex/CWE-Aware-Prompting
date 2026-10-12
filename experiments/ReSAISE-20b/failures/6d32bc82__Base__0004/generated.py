import json
from typing import Any

__all__ = ["deserialize_stream_data"]

# A minimal set of formats that are considered safe for deserialization.
# If you want to add more, make sure the corresponding loader is secure
# and does not execute arbitrary code.
ALLOWED_FORMATS = {
    "json": _json_loader,
}

def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Convert a serialized byte stream into the corresponding Python object.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    serialization_format : str
        The format of the data. Only formats listed in ALLOWED_FORMATS are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not supported or unsafe.
    """
    if not isinstance(stream, bytes):
        raise TypeError("stream must be a bytes object")

    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format!r}")

    loader = ALLOWED_FORMATS[fmt]
    return loader(stream)


def _json_loader(data: bytes) -> Any:
    """
    Safely load JSON data from a byte stream.
    """
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF-8") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data") from exc