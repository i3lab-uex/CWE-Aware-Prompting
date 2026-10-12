import json
import xml.etree.ElementTree as ET
from typing import Any

# A minimal, safe XML deserializer that returns a dictionary representation.
def _xml_to_dict(element: ET.Element) -> Any:
    """
    Recursively converts an ElementTree element into a dictionary.
    Text nodes are returned as strings; child elements become dict entries.
    """
    # If element has no children, return its text (stripped of whitespace)
    if len(element) == 0:
        return element.text.strip() if element.text else None

    result = {}
    for child in element:
        # If a tag appears multiple times, store it as a list
        key = child.tag
        value = _xml_to_dict(child)
        if key in result:
            # Existing entry: convert to list or append
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value
    return result


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize `serialized_bytes` according to the specified format.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw bytes containing the serialized data.
    allowed_format : str
        One of 'json' or 'xml'. Any other format will raise ValueError.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If the format is not supported or if deserialization fails.
    """
    fmt = allowed_format.lower()

    try:
        if fmt == "json":
            # json.loads accepts str, so decode bytes using UTF-8
            return json.loads(serialized_bytes.decode("utf-8"))

        elif fmt == "xml":
            # Parse the XML from bytes
            root = ET.fromstring(serialized_bytes)
            return _xml_to_dict(root)

        else:
            raise ValueError(f"Unsupported format: {allowed_format}")

    except (json.JSONDecodeError, ET.ParseError, UnicodeDecodeError) as exc:
        # Wrap parsing errors in ValueError to keep a consistent exception type
        raise ValueError(f"Deserialization failed for format {allowed_format}: {exc}") from exc