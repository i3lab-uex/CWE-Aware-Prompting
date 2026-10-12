import json
from typing import Any

# If you want to support additional safe formats, add them here.
# Each format must have a corresponding deserialization function
ALLOWED_FORMATS = {
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
        ``ALLOWED_FORMATS`` are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested serialization format is not supported or considered unsafe.
    """
    if not isinstance(byte_data, (bytes, bytearray)):
        raise TypeError("byte_data must be bytes or bytearray")

    if serialization_type not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: {serialization_type!r}. "
            f"Allowed formats are: {', '.join(ALLOWED_FORMATS)}"
        )

    # Decode bytes to string if needed
    try:
        decoded = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "byte_data could not be decoded using UTF-8; it may not be a valid text format."
        ) from exc

    # Call the deserializer
    deserializer = ALLOWED_FORMATS[serialization_type]
    try:
        return deserializer(decoded)
    except Exception as exc:  # pylint: disable=broad-except
        raise ValueError(f"Failed to deserialize data as {serialization_type!r}") from exc