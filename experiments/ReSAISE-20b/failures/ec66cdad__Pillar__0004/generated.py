import json
import html
from typing import Any


def restore_object_from_stream(byte_data: bytes, serialization_type: str) -> Any:
    """
    Safely deserialize a byte stream into a Python object.

    Parameters
    ----------
    byte_data : bytes
        The serialized data.
    serialization_type : str
        The format of the serialized data. Only formats listed in
        ``_ALLOWED_FORMATS`` are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If ``serialization_type`` is not in the list of allowed formats.
    """
    _ALLOWED_FORMATS = {
        "json",
        # Future safe formats could be added here, e.g. "yaml"
    }

    if serialization_type not in _ALLOWED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe serialization type: {serialization_type!r}"
        )

    if serialization_type == "json":
        # Decode bytes to text using UTF-8; errors are replaced to avoid crashes.
        text = byte_data.decode("utf-8", errors="replace")
        return json.loads(text)

    # If new formats are added, handle them here.
    raise ValueError(f"Unhandled serialization type: {serialization_type!r}")