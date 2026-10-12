import json
from typing import Any

# List of formats that are considered safe for deserialization.
ALLOWED_FORMATS = {"json"}

def deserialize_stream_data(stream: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    known safe formats.

    Parameters
    ----------
    stream : bytes
        The serialized byte stream.
    serialization_format : str
        The format of the serialized data (e.g., 'json').

    Returns
    -------
    Any
        The Python object reconstructed from the byte stream.

    Raises
    ------
    ValueError
        If an unsupported or unsafe format is requested.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization format: '{serialization_format}'. "
            f"Allowed formats are: {', '.join(sorted(ALLOWED_FORMATS))}"
        )

    # Currently only JSON is supported.
    if fmt == "json":
        try:
            decoded = stream.decode("utf-8")
            return json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc

    # Future formats can be added here with safe handling logic.