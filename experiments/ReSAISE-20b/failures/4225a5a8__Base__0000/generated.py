import json
import xml.etree.ElementTree as ET

def objectify_data(raw_data: bytes, method_name: str):
    """
    Safely deserialize data from a restricted set of formats.

    Parameters
    ----------
    raw_data : bytes
        Serialized data.
    method_name : str
        Name of the serialization format ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially dangerous.
    """
    if not isinstance(raw_data, (bytes, bytearray)):
        raise ValueError("raw_data must be bytes or bytearray")

    fmt = method_name.lower()

    if fmt == "json":
        try:
            # decode assuming UTF-8, ignore errors to avoid raising UnicodeDecodeError
            text = raw_data.decode("utf-8", errors="strict")
            return json.loads(text)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    elif fmt == "xml":
        try:
            # Parse XML into an ElementTree element.
            # ET.fromstring does not process external entities, mitigating XXE attacks.
            root = ET.fromstring(raw_data)
            return _xml_to_dict(root)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    else:
        # Disallow any other format, including pickle
        raise ValueError(f"Unsupported or dangerous serialization format: {method_name}")

def _xml_to_dict(element):
    """
    Convert an ElementTree element into a nested dictionary.
    Attributes are prefixed with '@', text content is stored under '#text'.
    """
    result = {}
    # Include attributes
    for key, value in element.attrib.items():
        result[f"@{key}"] = value

    # Process child elements
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_obj = _xml_to_dict(child)
            tag = child.tag
            if tag in child_dict:
                # Multiple children with same tag -> list
                if not isinstance(child_dict[tag], list):
                    child_dict[tag] = [child_dict[tag]]
                child_dict[tag].append(child_obj)
            else:
                child_dict[tag] = child_obj
        result.update(child_dict)

    # Include text content if present and not just whitespace
    text = element.text.strip() if element.text else ""
    if text:
        result["#text"] = text

    return result