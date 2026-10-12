import json
import xml.etree.ElementTree as ET
from typing import Any

def _safe_parse_xml(data: bytes) -> Any:
    """
    Parse XML data into a nested Python dict/list structure.
    This function intentionally limits the parsed content to avoid
    executing any code or loading external entities. It only handles
    simple elements and attributes, ignoring namespaces.
    """
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError("Invalid XML data") from exc

    def _element_to_obj(elem: ET.Element) -> Any:
        # Convert attributes to a dict
        obj = {"@attributes": elem.attrib} if elem.attrib else {}
        # Convert child elements
        children = [ _element_to_obj(e) for e in elem ]
        if children:
            obj[elem.tag] = children
        else:
            # Use text content if no children
            obj[elem.tag] = elem.text.strip() if elem.text else None
        return obj

    return _element_to_obj(root)


def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize `raw_data` according to the specified `method_name`.

    Supported formats (safe only):
        * 'json' : standard JSON deserialization.
        * 'xml'  : limited XML parsing into a dict/list structure.

    Any other method, especially pickle or marshal, will raise ValueError
    to prevent unsafe deserialization of untrusted data.

    Parameters:
        raw_data   : bytes containing the serialized representation.
        method_name: str specifying the serialization format.

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: if the method is unsupported or dangerous.
    """
    # Normalise method name to avoid case‑sensitive issues
    fmt = method_name.strip().lower()

    if fmt == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        return _safe_parse_xml(raw_data)

    # Disallow any other format to mitigate CWE‑502
    raise ValueError(f"Unsupported or unsafe deserialization method: {method_name}")