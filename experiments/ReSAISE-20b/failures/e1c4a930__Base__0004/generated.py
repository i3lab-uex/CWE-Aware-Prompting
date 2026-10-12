import json
from typing import Any


def deserialize_stream_payload(serialized_data: bytes, data_format_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Only JSON format is considered safe. All other formats raise ValueError.
    
    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    data_format_type : str
        The format of the serialized data (e.g., 'json', 'html', 'pickle').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or insecure.
    """
    # Normalize the format string to avoid case‑sensitivity issues
    fmt = data_format_type.strip().lower()

    if fmt != "json":
        raise ValueError(f"Unsupported or insecure format: {data_format_type!r}")

    try:
        # Decode bytes to string using UTF‑8 (common for JSON)
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8 encoded JSON") from exc

    try:
        # json.loads will raise a ValueError/JSONDecodeError on invalid JSON
        return json.loads(text)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError("Invalid JSON payload") from exc