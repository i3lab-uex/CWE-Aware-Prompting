import json
from typing import Any

def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        The format of the serialization. Supported values are:
            - 'json'   (case‑insensitive)

    Returns
    -------
    Any
        The Python object reconstructed from the serialized content.

    Raises
    ------
    ValueError
        If `input_format` is not supported or considered insecure.
    """
    if not isinstance(input_data, (bytes, bytearray)):
        raise TypeError("input_data must be bytes or bytearray")

    fmt = input_format.lower()

    if fmt == "json":
        try:
            # Decode bytes to string using UTF‑8 (common for JSON)
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF‑8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # If we reach here, the format is unsupported or insecure
    raise ValueError(f"Unsupported or insecure input format: {input_format}")