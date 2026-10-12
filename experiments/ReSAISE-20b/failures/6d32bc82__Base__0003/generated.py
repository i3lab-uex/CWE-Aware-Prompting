import json
from typing import Any


def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object for a known, secure format.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream to be deserialized.
    serialization_format : str
        Format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or deserialization fails.
    """
    # Define a whitelist of safe formats
    allowed_formats = {"json"}

    fmt = serialization_format.lower()
    if fmt not in allowed_formats:
        raise ValueError(
            f"Unsupported or unsafe serialization format: {serialization_format!r}. "
            f"Allowed formats are: {', '.join(sorted(allowed_formats))}."
        )

    try:
        # json.loads expects a str, not bytes
        return json.loads(stream.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"Failed to deserialize stream using format '{serialization_format}': {exc}"
        ) from exc