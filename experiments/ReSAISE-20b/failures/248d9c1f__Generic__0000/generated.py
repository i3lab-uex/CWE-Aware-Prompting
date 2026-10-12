import json
import xml.etree.ElementTree as ET
from typing import Any

try:
    # PyYAML is optional; if not installed we simply don't support yaml
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _xml_to_dict(element: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a nested dictionary.
    Text content is stored under the key '#text'.
    Attributes are prefixed with '@'.
    """
    d = {}
    # Process attributes
    for attr, value in element.attrib.items():
        d[f"@{attr}"] = value

    # Process child elements
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_name = child.tag
            child_obj = _xml_to_dict(child)
            if child_name in child_dict:
                # Ensure multiple children with same tag become a list
                if not isinstance(child_dict[child_name], list):
                    child_dict[child_name] = [child_dict[child_name]]
                child_dict[child_name].append(child_obj)
            else:
                child_dict[child_name] = child_obj
        d.update(child_dict)

    # Process text content
    text = element.text.strip() if element.text else ""
    if text:
        d["#text"] = text

    return d


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize a byte string into a Python object.

    Parameters
    ----------
    byte_data : bytes
        Serialized data.
    encoding_type : str
        The format of the serialized data. Supported values are:
        - 'json'   : JSON
        - 'xml'    : XML (converted to a nested dict)
        - 'yaml'   : YAML using safe_load

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the encoding_type is not supported or dangerous.
    """
    if not isinstance(byte_data, bytes):
        raise TypeError("byte_data must be of type 'bytes'")

    fmt = encoding_type.lower()
    if fmt == "json":
        return json.loads(byte_data.decode("utf-8"))
    elif fmt == "xml":
        root = ET.fromstring(byte_data.decode("utf-8"))
        return _xml_to_dict(root)
    elif fmt == "yaml":
        if yaml is None:
            raise ValueError("PyYAML not installed; YAML support unavailable.")
        return yaml.safe_load(byte_data.decode("utf-8"))
    else:
        raise ValueError(f"Unsupported or unsafe format: {encoding_type}")