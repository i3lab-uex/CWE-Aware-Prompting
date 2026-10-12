import json
from typing import Any

# Define the list of serialization formats that are considered safe.
SAFE_SERIALIZATION_TYPES = {"json"}

def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data stream.
    serialization_type : str
        Format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization_type is not in the list of allowed safe formats.
    """
    # Normalize the format string to lowercase for comparison
    fmt = serialization_type.strip().lower()

    if fmt not in SAFE_SERIALIZATION_TYPES:
        raise ValueError(
            f"Unsupported or unsafe serialization format: '{serialization_type}'. "
            f"Allowed formats are: {', '.join(SAFE_SERIALIZATION_TYPES)}."
        )

    # For JSON, decode bytes to text and parse
    if fmt == "json":
        try:
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"Byte data could not be decoded to UTF-8: {e}") from e

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}") from e

    # If the format list is expanded in future, add handlers here.