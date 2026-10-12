import json
from typing import Any


# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json"}


def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize `content` based on the specified `format_type`.

    Parameters
    ----------
    content : bytes
        The serialized data to be deserialized.
    format_type : str
        Format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object obtained after deserialization.

    Raises
    ------
    ValueError
        If the format is unsupported or deemed insecure.
    """
    if format_type not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure format: {format_type}")

    if format_type == "json":
        try:
            # Assume UTF-8 encoding for JSON payloads
            decoded = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Content is not valid UTF-8 encoded JSON") from exc

        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # Future safe formats can be added here
    raise ValueError(f"Format handler for '{format_type}' is not implemented")