import json
from typing import Any

__ALLOWED_FORMATS = {"json"}

def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes raw data that is known to be in a permitted format.

    Parameters
    ----------
    raw_data : bytes
        Serialized representation of the object.
    serialization_format : str
        The name of the format used for serialization (e.g., 'json').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist of safe formats.
    """
    fmt = serialization_format.lower()
    if fmt not in __ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe serialization format: {serialization_format}")

    if fmt == "json":
        # json.loads expects a str, so decode bytes using UTF-8.
        try:
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Input bytes are not valid UTF-8 encoded JSON") from exc

        # json.loads is safe for trusted data; it never executes arbitrary code.
        return json.loads(text)

    # The code path should never reach here because only 'json' is allowed.
    raise ValueError(f"Unhandled format: {serialization_format}")