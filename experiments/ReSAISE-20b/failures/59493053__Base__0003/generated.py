import json
from typing import Any

# Only the following formats are considered safe and allowed.
ALLOWED_FORMATS = {"json"}

def deserialize_data(input_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte sequence into a Python object using only safe formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte form.
    serialization_format : str
        Format used for serialization. Only 'json' is permitted.

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict, list, str, int, etc.).

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    try:
        # json.loads accepts str, so decode bytes using UTF-8.
        text = input_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8 encoded JSON") from exc

    try:
        # json.loads will raise a ValueError if the data is not valid JSON.
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Input data is not valid JSON") from exc