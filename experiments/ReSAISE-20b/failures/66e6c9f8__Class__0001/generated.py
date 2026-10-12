import json
from typing import Any

# A whitelist of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json": json.loads,
}

def deserialize_content_stream(stream: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized data.
    stream_format : str
        Format identifier, e.g. 'json'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the whitelist or if deserialization fails.
    """
    # Normalise the format string
    fmt = stream_format.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {stream_format}")

    # Decode bytes to string for JSON parsing
    try:
        data_str = stream.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Failed to decode input bytes") from exc

    # Perform deserialization using the selected handler
    try:
        return SAFE_FORMATS[fmt](data_str)
    except Exception as exc:  # pragma: no cover
        raise ValueError("Deserialization error") from exc