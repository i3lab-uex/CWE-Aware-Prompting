import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

# Allowed serialization formats
ALLOWED_FORMATS = {"json", "xml"}


def _etree_to_dict(element: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an ElementTree element into a dictionary.
    Text content is stored under the key '#text'.
    Attributes are prefixed with '@' to distinguish them.
    Child elements are added as nested dictionaries or lists when multiple
    children share the same tag name.
    """
    def _convert(e: ET.Element) -> Any:
        # Process attributes
        result = {f"@{k}": v for k, v in e.attrib.items()}

        # Process child elements
        children = list(e)
        if children:
            child_dict: Dict[str, Any] = {}
            for child in children:
                child_res = _convert(child)
                tag = child.tag
                if tag in child_dict:
                    # Existing entry: convert to list
                    if not isinstance(child_dict[tag], list):
                        child_dict[tag] = [child_dict[tag]]
                    child_dict[tag].append(child_res)
                else:
                    child_dict[tag] = child_res
            result.update(child_dict)

        # Process text content
        text = e.text.strip() if e.text else ""
        if text:
            result["#text"] = text

        return result

    return _convert(element)


def deserialize_data(raw_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes `raw_data` according to the specified
    `serialization_format`. Only formats listed in ALLOWED_FORMATS are
    supported. Unsupported or unsafe formats raise a ValueError.

    Parameters:
        raw_data (bytes): The serialized data.
        serialization_format (str): Format of the data ('json', 'xml').

    Returns:
        The deserialized Python object (dict, list, etc.).

    Raises:
        ValueError: If the format is not supported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported serialization format: {serialization_format!r}")

    try:
        if fmt == "json":
            # json.loads expects a str, so decode using UTF-8
            return json.loads(raw_data.decode("utf-8"))
        elif fmt == "xml":
            root = ET.fromstring(raw_data)
            return _etree_to_dict(root)
    except Exception as exc:
        # Wrap any exception in a ValueError to avoid leaking internal errors
        raise ValueError(f"Failed to deserialize data as {serialization_format}: {exc}") from exc