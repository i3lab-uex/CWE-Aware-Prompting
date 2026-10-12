import json
from typing import Any

def deserialize_data(input_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize serialized data from a trusted set of formats.

    Parameters
    ----------
    input_data : bytes
        Serialized object represented in byte format.
    serialization_format : str
        The name of the serialization format used. Supported values are:
        - 'json'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered dangerous.
    """
    # Define a whitelist of safe formats
    SAFE_FORMATS = {"json"}

    fmt_lower = serialization_format.lower()
    if fmt_lower not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or dangerous serialization format: {serialization_format!r}")

    if fmt_lower == "json":
        # json.loads accepts a str, so decode bytes safely
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input data is not valid UTF-8 encoded JSON") from exc

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # If additional formats are added in the future, they must be handled explicitly
    raise ValueError(f"Deserialization for format {serialization_format!r} is not implemented")