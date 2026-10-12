import json
import xml.etree.ElementTree as ET
from typing import Any, Dict


# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "xml"}


def _parse_xml_element(elem: ET.Element) -> Dict[str, Any]:
    """
    Recursively convert an XML element into a nested dictionary.
    Attributes are stored under the key '@attributes'.
    Text content is stored under the key '#text' if present.
    Child elements are represented as lists when multiple children share
    the same tag name, otherwise as a single dictionary.
    """
    parsed: Dict[str, Any] = {}

    # Handle attributes
    if elem.attrib:
        parsed["@attributes"] = dict(elem.attrib)

    # Handle text content
    text = elem.text.strip() if elem.text else ""
    if text:
        parsed["#text"] = text

    # Handle child elements
    children_by_tag: Dict[str, Any] = {}
    for child in elem:
        child_parsed = _parse_xml_element(child)
        tag = child.tag
        if tag in children_by_tag:
            # Convert to list if multiple children with the same tag
            if not isinstance(children_by_tag[tag], list):
                children_by_tag[tag] = [children_by_tag[tag]]
            children_by_tag[tag].append(child_parsed)
        else:
            children_by_tag[tag] = child_parsed

    parsed.update(children_by_tag)
    return parsed


def load_serialized_data(bytes_data: bytes, data_format: str) -> Any:
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        The raw serialized data.
    data_format : str
        One of the supported formats: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If `data_format` is not in the set of supported formats.
    """
    fmt = data_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format}")

    if fmt == "json":
        try:
            # json.loads accepts str; decode bytes using utf-8
            return json.loads(bytes_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON data: {exc}") from exc

    if fmt == "xml":
        try:
            root = ET.fromstring(bytes_data)
            return {root.tag: _parse_xml_element(root)}
        except ET.ParseError as exc:
            raise ValueError(f"Failed to parse XML data: {exc}") from exc

    # The code should never reach here because of the earlier check
    raise ValueError(f"Unhandled format: {data_format}")