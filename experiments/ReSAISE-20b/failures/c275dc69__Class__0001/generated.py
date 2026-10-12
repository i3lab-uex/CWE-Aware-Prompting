import json
from typing import Any

def deserialize_stream(serialized_data: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream that contains the serialized data.
    stream_format : str
        The format of the serialized data. Only 'json' is supported.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If the specified format is unsupported or considered insecure.
    """
    # Normalize format string to avoid case‑sensitivity issues
    fmt = stream_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to text using UTF‑8; raise if decoding fails
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 data for JSON deserialization: {exc}") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON deserialization error: {exc}") from exc

    # Future safe formats can be added here
    # e.g., if fmt == "msgpack": ...

    raise ValueError(f"Unsupported or insecure format: '{stream_format}'. "
                     "Only 'json' is allowed for deserialization.")