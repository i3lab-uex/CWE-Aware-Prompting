import json
from typing import Any

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {
    "json": json.loads,
}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object only if the format is trusted.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        The name of the serialization format (e.g. 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `format_type` is not in the list of trusted formats.
    """
    # Normalize format name to lower case for comparison
    fmt = format_type.lower()

    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    # Get the deserializer function
    deserializer = SAFE_FORMATS[fmt]

    try:
        # For JSON, bytes must be decoded to a string
        if fmt == "json":
            data_str = content.decode("utf-8")
            return deserializer(data_str)
        else:
            # If new formats are added that don't require decoding,
            # they can be handled here.
            return deserializer(content)
    except Exception as exc:
        # Wrap any exception in a ValueError to avoid leaking internal errors
        raise ValueError(f"Failed to deserialize content: {exc}") from exc