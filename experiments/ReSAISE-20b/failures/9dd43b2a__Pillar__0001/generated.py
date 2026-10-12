import json
from typing import Any

# List of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json": json.loads,
}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize the given byte stream into a Python object if the format is trusted.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object restored from the serialized data.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Normalise format_type to lower case for comparison
    fmt = format_type.lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Retrieve the appropriate deserializer
    deserializer = SAFE_FORMATS[fmt]

    try:
        # For JSON we need to decode bytes to str
        if fmt == "json":
            text = content.decode("utf-8")
            return deserializer(text)
        # If new safe formats are added, they can be handled here
    except Exception as exc:
        raise ValueError(f"Failed to deserialize content: {exc}") from exc

    # If we reach here, something went wrong
    raise ValueError(f"Deserialization for format '{format_type}' failed.")