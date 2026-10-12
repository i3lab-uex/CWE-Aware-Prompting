import json
from typing import Any

def decode_serialized_input(input_data: bytes, input_format: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only secure, predefined formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data to be deserialized.
    input_format : str
        The format of the serialized data. Supported values are:
            * 'json'  – JSON text encoded in UTF‑8.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the requested format is unsupported or insecure, or if deserialization fails.
    """
    # Normalize format name
    fmt = input_format.strip().lower()

    if fmt == "json":
        try:
            # Decode bytes to string (UTF‑8) with strict error handling
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data must be valid UTF‑8") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON") from exc

    # Future extensions could add other safe formats here (e.g., msgpack, yaml‑safe)

    raise ValueError(f"Unsupported or insecure format: {input_format!r}")