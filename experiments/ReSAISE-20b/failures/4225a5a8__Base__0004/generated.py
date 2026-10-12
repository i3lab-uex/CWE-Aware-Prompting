import json
import xml.etree.ElementTree as ET
from typing import Any

def _xml_to_dict(elem: ET.Element) -> dict:
    """
    Recursively convert an ElementTree element into a dictionary.
    This implementation is intentionally simple and only supports
    elements with text content or nested elements. Attributes are ignored.
    """
    if len(elem) == 0:  # leaf node
        return {elem.tag: elem.text.strip() if elem.text else None}
    result = {}
    for child in elem:
        child_dict = _xml_to_dict(child)
        # merge dictionaries; if duplicate keys, keep as list
        for k, v in child_dict.items():
            if k in result:
                if not isinstance(result[k], list):
                    result[k] = [result[k]]
                result[k].append(v)
            else:
                result[k] = v
    return {elem.tag: result}

def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize `raw_data` according to the specified `method_name`.
    
    Supported formats:
        - 'json': JSON text (UTF-8 encoded)
        - 'xml' : Simple XML (converted to a nested dictionary)
    
    Raises:
        ValueError: if the method_name is unsupported or deserialization fails.
    """
    if not isinstance(raw_data, bytes):
        raise TypeError("raw_data must be of type 'bytes'")

    method = method_name.lower()
    try:
        if method == "json":
            text = raw_data.decode("utf-8")
            return json.loads(text)
        elif method == "xml":
            text = raw_data.decode("utf-8")
            root = ET.fromstring(text)
            return _xml_to_dict(root)
        else:
            raise ValueError(f"Unsupported or dangerous format: {method_name}")
    except (UnicodeDecodeError, json.JSONDecodeError, ET.ParseError) as exc:
        raise ValueError(f"Deserialization failed for format '{method_name}': {exc}") from exc