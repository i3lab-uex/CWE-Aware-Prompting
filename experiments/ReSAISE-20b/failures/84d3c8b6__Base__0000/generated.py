import json
import xml.etree.ElementTree as ET
import pickle
from typing import Any, Dict

# A whitelist of safe built-in types for pickle deserialization
_SAFE_BUILTINS = {
    'builtins.int',
    'builtins.str',
    'builtins.float',
    'builtins.bool',
    'builtins.list',
    'builtins.dict',
    'builtins.tuple',
    'builtins.set',
    'builtins.frozenset',
    'builtins.bytes',
}

class _SafeUnpickler(pickle.Unpickler):
    """
    A custom Unpickler that only allows loading of safe built-in types.
    Any attempt to load a class not in the whitelist will raise an exception.
    """
    def find_class(self, module: str, name: str):
        full_name = f'{module}.{name}'
        if full_name not in _SAFE_BUILTINS:
            raise pickle.UnpicklingError(f"Disallowed class {full_name}")
        return super().find_class(module, name)

def _deserialize_pickle(encoded_data: bytes) -> Any:
    """
    Deserialize pickle data using a restricted unpickler.
    """
    return _SafeUnpickler(encoded_data).load()

def _deserialize_xml(encoded_data: bytes) -> Any:
    """
    Deserialize XML data into a nested dictionary.
    This implementation does not support attributes or namespaces for simplicity
    and to keep the output predictable.
    """
    root = ET.fromstring(encoded_data.decode('utf-8'))
    
    def elem_to_dict(elem: ET.Element) -> Any:
        # If the element has no children, return its text (or None)
        if len(elem) == 0:
            return elem.text
        # If the element has children, build a dict/list representation
        child_dict: Dict[str, Any] = {}
        for child in elem:
            key = child.tag
            value = elem_to_dict(child)
            if key in child_dict:
                # Convert to list if multiple children with same tag
                existing = child_dict[key]
                if not isinstance(existing, list):
                    child_dict[key] = [existing]
                child_dict[key].append(value)
            else:
                child_dict[key] = value
        return child_dict
    
    return {root.tag: elem_to_dict(root)}

def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize `encoded_data` according to the specified `method`.
    
    Supported methods:
        - 'json': JSON format
        - 'xml' : XML format (converted to nested dict)
        - 'pickle': Python pickle format (restricted to safe built-ins)
    
    Raises:
        ValueError: If an unsupported or unsafe method is requested.
    """
    if not isinstance(encoded_data, bytes):
        raise TypeError("encoded_data must be of type 'bytes'")

    method = method.lower()
    
    if method == 'json':
        try:
            return json.loads(encoded_data.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc
    
    if method == 'xml':
        try:
            return _deserialize_xml(encoded_data)
        except ET.ParseError as exc:
            raise ValueError(f"Invalid XML data: {exc}") from exc
    
    if method == 'pickle':
        try:
            return _deserialize_pickle(encoded_data)
        except (pickle.UnpicklingError, EOFError) as exc:
            raise ValueError(f"Invalid or unsafe pickle data: {exc}") from exc
    
    raise ValueError(f"Unsupported deserialization method '{method}'. "
                     "Allowed methods are: 'json', 'xml', 'pickle'.")