import json
import xml.etree.ElementTree as ET
from typing import Any, Dict

# Define the set of allowed data formats for safe deserialization
ALLOWED_FORMATS = {"json", "xml"}


def _element_to_dict(element: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an XML Element into a nested dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    """
    node: Dict[str, Any] = {}

    # Handle element attributes
    if element.attrib:
        node["@attributes"] = dict(element.attrib)

    # Handle text content
    text = element.text.strip() if element.text else ""
    if text:
        node["#text"] = text

    # Handle child elements
    children = list(element)
    if children:
        child_dict: Dict[str, Any] = {}
        for child in children:
            child_key = child.tag
            child_value = _element_to_dict(child)
            if child_key in child_dict:
                # If the key already exists, convert to a list
                if not isinstance(child_dict[child_key], list):
                    child_dict[child_key] = [child_dict[child_key]]
                child_dict[child_key].append(child_value)
            else:
                child_dict[child_key] = child_value
        node.update(child_dict)

    return node


def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `bytes_data` based on the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        The raw serialized data.
    data_format : str
        Format of the serialization. Must be one of ALLOWED_FORMATS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or unsafe.
    """
    # Normalise the format string for comparison
    fmt = data_format.strip().lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format}")

    if fmt == "json":
        # Decode bytes to string and parse JSON
        try:
            text = bytes_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if fmt == "xml":
        # Parse XML and convert to a dictionary
        try:
            root = ET.fromstring(bytes_data)
            return {root.tag: _element_to_dict(root)}
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled data format: {data_format}")