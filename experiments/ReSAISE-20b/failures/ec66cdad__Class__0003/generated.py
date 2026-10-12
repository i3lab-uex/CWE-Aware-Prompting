import json
from typing import Any

def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Only the following serialization formats are considered safe:
        - 'json'

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
        If an unsupported or unsafe serialization format is requested.
    """
    # Normalise the type string
    fmt = serialization_type.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF-8
            text = byte_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF-8 data for JSON deserialization: {exc}") from exc

        try:
            # Use json.loads which does not execute arbitrary code
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Failed to parse JSON data: {exc}") from exc

    # If the format is not in the allowed list, raise an error
    raise ValueError(f"Unsupported or unsafe serialization format: '{serialization_type}'. "
                     "Only 'json' is allowed.")