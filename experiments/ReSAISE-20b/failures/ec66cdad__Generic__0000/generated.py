import json
from typing import Any

# A mapping of allowed serialization formats to the functions that can safely load them.
ALLOWED_LOADERS = {
    "json": json.loads,
}

def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The format of the serialized data. Only formats listed in
        `ALLOWED_LOADERS` are accepted.

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe serialization format is requested,
        or if the byte stream cannot be decoded/parsed.
    """
    # Normalise the format name (case‑insensitive)
    fmt = serialization_type.strip().lower()

    if fmt not in ALLOWED_LOADERS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_type}")

    # Decode the bytes to a string. UTF‑8 is assumed for all safe formats.
    try:
        text = byte_data.decode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to decode byte stream as UTF‑8: {exc}") from exc

    # Perform the actual deserialization
    loader = ALLOWED_LOADERS[fmt]
    try:
        return loader(text)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Deserialization error for format '{serialization_type}': {exc}") from exc