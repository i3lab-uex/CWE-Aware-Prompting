import json
from typing import Any

def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize raw bytes into a Python object using only trusted formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte form.
    data_type : str
        The serialization format. Supported values are:
            - 'json'   (case‑insensitive)

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the data_type is not supported or if deserialization fails.
    """
    # Normalise format name
    fmt = data_type.strip().lower()

    if fmt != "json":
        raise ValueError(f"Unsupported or unsafe format '{data_type}'. Only 'json' is allowed.")

    try:
        # Decode bytes to string safely using UTF‑8 with strict error handling
        text = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8.") from exc

    try:
        # json.loads never executes code, so it is safe for untrusted data
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Failed to parse JSON data.") from exc