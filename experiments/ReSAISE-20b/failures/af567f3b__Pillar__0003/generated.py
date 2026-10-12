import json
from typing import Any

def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize the given byte stream into a Python object using only
    safe, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        Deserialization format. Currently only 'json' is supported.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format is unsupported or insecure.
    """
    # Normalise input format string to avoid case‑sensitive mismatches
    fmt = input_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF‑8 before parsing
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid UTF‑8 input for JSON: {exc}") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed JSON data: {exc}") from exc

    # Add any additional safe formats here in the future
    # e.g., 'msgpack', 'yaml' with a safe loader, etc.

    raise ValueError(f"Unsupported or insecure format: '{input_format}'. "
                     "Only 'json' is allowed.")