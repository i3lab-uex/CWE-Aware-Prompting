import json
from typing import Any

def deserialize_content(data: bytes, data_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only
    secure, predefined formats.

    Parameters
    ----------
    data : bytes
        The serialized byte stream.
    data_format : str
        The serialization format. Currently only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json"}

    fmt_lower = data_format.lower()
    if fmt_lower not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or insecure format '{data_format}'. "
            f"Allowed formats: {', '.join(SAFE_FORMATS)}."
        )

    # For JSON, decode bytes to string and parse
    if fmt_lower == "json":
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data is not valid UTF-8 encoded JSON.") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON content.") from exc