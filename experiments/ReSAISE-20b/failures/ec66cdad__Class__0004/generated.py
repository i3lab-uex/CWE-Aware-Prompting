import json
from typing import Any


# --------------------------------------------------------------------------- #
# Safe deserialization helper
# --------------------------------------------------------------------------- #

ALLOWED_FORMATS = {
    "json": json.loads,
    # Additional safe formats can be added here if desired
}

def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    known, safe formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is not in the list of allowed formats.
    """
    if serialization_type not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization type: {serialization_type!r}"
        )

    # Retrieve the deserializer function
    deserializer = ALLOWED_FORMATS[serialization_type]

    try:
        if serialization_type == "json":
            # json.loads expects a string, so decode bytes first
            return deserializer(byte_data.decode("utf-8"))
        else:
            # For any future formats that accept bytes directly
            return deserializer(byte_data)
    except Exception as exc:
        # Wrap any exception to avoid leaking internal details
        raise ValueError(
            f"Failed to deserialize data with type {serialization_type!r}"
        ) from exc