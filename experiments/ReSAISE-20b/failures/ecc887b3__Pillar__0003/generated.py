import json
import xml.etree.ElementTree as ET

# Whitelisted formats for safe deserialization
_ALLOWED_FORMATS = {"json", "xml"}

def safe_deserialize(serialized_bytes: bytes, allowed_format: str):
    """
    Safely deserialize `serialized_bytes` according to the specified
    `allowed_format`. Only formats in _ALLOWED_FORMATS are permitted.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte sequence containing the serialized data.
    allowed_format : str
        The serialization format used (e.g., 'json', 'xml').

    Returns
    -------
    object
        The deserialized Python object (e.g., dict, list, ElementTree).

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    # Validate format
    fmt = allowed_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    # Ensure input is bytes
    if not isinstance(serialized_bytes, (bytes, bytearray)):
        raise ValueError("Input must be bytes or bytearray")

    try:
        if fmt == "json":
            # Decode UTF‑8 and parse JSON
            text = serialized_bytes.decode("utf-8")
            return json.loads(text)

        elif fmt == "xml":
            # Parse XML safely using ElementTree (no external entities)
            return ET.fromstring(serialized_bytes)

    except Exception as exc:
        # Wrap any parsing exception in ValueError for consistency
        raise ValueError(f"Deserialization error ({fmt}): {exc}") from exc

# Example usage:
if __name__ == "__main__":
    # JSON example
    json_bytes = b'{"key": "value", "list": [1, 2, 3]}'
    obj = safe_deserialize(json_bytes, "json")
    print(obj)  # {'key': 'value', 'list': [1, 2, 3]}

    # XML example
    xml_bytes = b'<root><child>text</child></root>'
    elem = safe_deserialize(xml_bytes, "xml")
    print(ET.tostring(elem))  # b'<root><child>text</child></root>'