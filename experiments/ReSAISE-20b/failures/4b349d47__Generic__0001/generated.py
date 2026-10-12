import json
import xml.etree.ElementTree as ET
import pickle

# Predefined set of allowed formats for deserialization
ALLOWED_FORMATS = {"json", "xml", "pickle"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Convert serialized data back into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The serialized object in byte form.
    format_type : str
        One of the permitted serialized data formats (e.g. 'json', 'xml',
        'pickle').

    Returns
    -------
    Any
        The deserialized Python object for valid formats.

    Raises
    ------
    ValueError
        If the supplied format_type is not in ALLOWED_FORMATS.
    """
    if format_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    # JSON deserialization
    if format_type.lower() == "json":
        try:
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    # XML deserialization
    if format_type.lower() == "xml":
        try:
            return ET.fromstring(serialized_data)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # Pickle deserialization (use with caution)
    if format_type.lower() == "pickle":
        try:
            return pickle.loads(serialized_data)
        except pickle.UnpicklingError as exc:
            raise ValueError(f"Invalid pickle data: {exc}") from exc

    # Should never reach here because of the earlier check
    raise ValueError(f"Unhandled format: {format_type}")