import json
from typing import Any

def deserialize_stream(serialized_data: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object in a secure manner.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream to be deserialized.
    stream_format : str
        The format of the serialized data. Currently only 'json' is supported.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If `stream_format` is not supported or considered insecure.
    """
    # Only allow JSON deserialization for safety
    allowed_formats = {"json"}

    if stream_format.lower() not in allowed_formats:
        raise ValueError(
            f"Unsupported or insecure format '{stream_format}'. "
            f"Allowed formats: {', '.join(sorted(allowed_formats))}"
        )

    # JSON requires a text string, so decode the bytes safely
    try:
        json_text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded as UTF-8.") from exc

    # Use json.loads with strict mode (default) to avoid arbitrary code execution
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON data.") from exc