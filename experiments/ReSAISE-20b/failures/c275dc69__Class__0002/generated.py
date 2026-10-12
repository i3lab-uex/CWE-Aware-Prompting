import json
from typing import Any

def deserialize_stream(serialized_data: bytes, stream_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    serialized_data : bytes
        The data to deserialize.
    stream_format : str
        The format of the serialized data. Supported values are:
            - 'json'  : safe JSON deserialization.
        Any other value will raise ValueError.

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If `stream_format` is unsupported or considered insecure.
    """
    # Normalize format string for case-insensitive comparison
    fmt = stream_format.strip().lower()

    if fmt == 'json':
        try:
            # Decode bytes to string using UTF-8 (common for JSON)
            text = serialized_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode JSON bytes: not valid UTF-8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # Add more safe formats here if needed, e.g. 'yaml' with ruamel.yaml.safe_load
    # but for this implementation only JSON is considered safe.

    raise ValueError(f"Unsupported or insecure stream format: {stream_format}")