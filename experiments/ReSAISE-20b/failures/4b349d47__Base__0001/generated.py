import json
import xml.etree.ElementTree as ET

# Define the set of trusted formats that are allowed to be deserialized
ALLOWED_FORMATS = {"json", "xml"}

def convert_to_object(serialized_data: bytes, format_type: str):
    """
    Convert serialized data back into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The raw serialized data.
    format_type : str
        One of the permitted formats ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python object.  For XML the returned object is an
        `xml.etree.ElementTree.Element` instance.

    Raises
    ------
    ValueError
        If the format_type is not in ALLOWED_FORMATS or if deserialization fails.
    """
    if format_type.lower() not in ALLOWED_FORMATS:
        raise ValueError(f"Untrusted or unsupported format: {format_type!r}")

    try:
        if format_type.lower() == "json":
            # json.loads expects a string, so decode bytes safely
            return json.loads(serialized_data.decode("utf-8"))
        elif format_type.lower() == "xml":
            # ET.fromstring parses XML into an ElementTree.Element
            return ET.fromstring(serialized_data.decode("utf-8"))
    except Exception as exc:
        # Wrap any parsing error in a ValueError to keep the API consistent
        raise ValueError(f"Failed to deserialize data as {format_type!r}") from exc