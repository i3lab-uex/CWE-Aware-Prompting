import json
from typing import Any


def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Safely deserialize a byte stream into a Python object.

    Supported formats (case‑insensitive):
        - 'json'   : JSON text

    All other formats raise a ValueError to avoid unsafe deserialization.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        The format of the serialized data ('json', etc.).

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered insecure.
    """
    # Normalize format string for comparison
    fmt = input_format.strip().lower()

    if fmt == "json":
        # Decode bytes to str using UTF‑8, then parse JSON.
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 data for JSON: {exc}") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    # Add more safe formats here if needed in the future.
    # For any other format, refuse to deserialize.
    raise ValueError(f"Unsupported or insecure deserialization format: {input_format}")