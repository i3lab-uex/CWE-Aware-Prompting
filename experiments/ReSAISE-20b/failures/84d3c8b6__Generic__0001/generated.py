import json
import xml.etree.ElementTree as ET
import pickle
from typing import Any


class SafeUnpickler(pickle.Unpickler):
    """
    A pickle.Unpickler that only allows loading of built‑in types.
    All other classes will raise an exception to prevent execution
    of malicious code.
    """
    def find_class(self, module: str, name: str):
        # Only allow built‑in modules (like 'builtins' or 'datetime' if needed)
        # Here we restrict to built‑in module
        if module != "builtins":
            raise pickle.UnpicklingError(
                f"Disallowed class {module}.{name} during unpickling"
            )
        # Delegate to the original find_class for built‑in types
        return super().find_class(module, name)


def _parse_xml_to_dict(element: ET.Element) -> Any:
    """
    Recursively convert an ElementTree element into a nested dict.
    Text nodes are stripped; attributes become a dictionary under '@attributes'.
    """
    node = {}
    # Handle element's attributes
    if element.attrib:
        node["@attributes"] = dict(element.attrib)

    # Process child elements
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_key = child.tag
            child_value = _parse_xml_to_dict(child)
            if child_key in child_dict:
                # If multiple children with same tag, store as list
                if not isinstance(child_dict[child_key], list):
                    child_dict[child_key] = [child_dict[child_key]]
                child_dict[child_key].append(child_value)
            else:
                child_dict[child_key] = child_value
        node.update(child_dict)

    # Handle text content (if any)
    text = element.text
    if text and text.strip():
        node["#text"] = text.strip()

    return node


def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize *encoded_data* according to the specified *method*.

    Supported methods: 'json', 'xml', 'pickle'.

    Raises:
        ValueError: If *method* is unsupported or dangerous.
        pickle.UnpicklingError: If pickle data contains disallowed classes.
    """
    method = method.lower()
    if method == "json":
        try:
            # Decode bytes to string using UTF-8
            return json.loads(encoded_data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "xml":
        try:
            root = ET.fromstring(encoded_data)
            return _parse_xml_to_dict(root)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    if method == "pickle":
        try:
            # Use the safe unpickler defined above
            return SafeUnpickler(io.BytesIO(encoded_data)).load()
        except pickle.UnpicklingError as exc:
            raise ValueError("Unsafe pickle data") from exc

    # Unsupported method
    raise ValueError(f"Unsupported or dangerous format: {method}")