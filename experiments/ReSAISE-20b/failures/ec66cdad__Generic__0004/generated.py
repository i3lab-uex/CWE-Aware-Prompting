import json
from typing import Any

# A set of serialization formats that are considered safe for deserialization.
# Add additional formats here only after a thorough security review.
ALLOWED_SERIALIZATIONS = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If the requested serialization format is not in the list of allowed formats,
        or if deserialization fails.
    """
    # Normalise the format string (case‑insensitive)
    fmt = serialization_type.strip().lower()

    if fmt not in ALLOWED_SERIALIZATIONS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_type!r}")

    try:
        if fmt == "json":
            # JSON expects a text stream; decode bytes to str first.
            return json.loads(byte_data.decode("utf-8"))
    except Exception as exc:
        # Re‑raise with a more descriptive message
        raise ValueError(f"Failed to deserialize data as {serialization_type!r}: {exc}") from exc