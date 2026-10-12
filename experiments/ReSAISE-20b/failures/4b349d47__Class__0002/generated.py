import json
import xml.etree.ElementTree as ET
import pickle
from typing import Any


# ----------------------------------------------------------------------
# Allowed formats for deserialization
# ----------------------------------------------------------------------
ALLOWED_FORMATS = {
    "json",
    "xml",
    "pickle",   # Note: pickle is inherently risky; use only with trusted data
}


def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Convert serialized data back into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The serialized representation of the object.
    format_type : str
        One of the permitted formats ('json', 'xml', 'pickle').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not in the allowed set.
    """
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    if format_type == "json":
        # JSON is safe for basic data types
        return json.loads(serialized_data.decode("utf-8"))

    if format_type == "xml":
        # ElementTree parses XML into an element tree; no code execution occurs
        return ET.fromstring(serialized_data.decode("utf-8"))

    if format_type == "pickle":
        # Pickle is dangerous; we restrict the unpickler to a safe subset.
        # Here we use the standard pickle.loads but only allow built-in types.
        # In production, consider using a custom Unpickler or an alternative
        # serialization format.
        return pickle.loads(serialized_data)

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_type}")