import json
from typing import Any

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json"}

def parse_serialized_content(content: bytes, format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object only for trusted formats.

    Parameters
    ----------
    content : bytes
        Serialized data to be deserialized.
    format_type : str
        The serialization format (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or deemed insecure.
    """
    if format_type.lower() not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type}")

    # Currently only JSON is supported
    if format_type.lower() == "json":
        try:
            # Decode bytes to string using UTF-8
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Content is not valid UTF-8 encoded JSON") from exc

        try:
            # Use json.loads which is safe for JSON data
            return json.loads(text, strict=True)
        except json.JSONDecodeError as exc:
            raise ValueError("Content is not valid JSON") from exc

    # Future safe formats can be added here
    raise ValueError(f"Format {format_type} is not implemented as safe")