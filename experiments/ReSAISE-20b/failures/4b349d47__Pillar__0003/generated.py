import json
import xml.etree.ElementTree as ET
import pickle
from typing import Any


# ------------------------------------------------------------------
# Restricted unpickler to mitigate unsafe deserialization (CWE-664)
# Only built‑in types and simple containers are allowed.
# ------------------------------------------------------------------
class RestrictedUnpickler(pickle.Unpickler):
    """
    Unpickler that only allows safe built‑in types.
    Raises pickle.UnpicklingError if an attempt is made to load
    a potentially unsafe or custom class.
    """
    SAFE_BUILTINS = {
        'builtins': (
            'list', 'tuple', 'dict', 'set', 'frozenset',
            'int', 'float', 'bool', 'str', 'bytes',
            'NoneType'
        )
    }

    def find_class(self, module: str, name: str):
        if (module, name) in self.SAFE_BUILTINS.items():
            return getattr(__import__(module), name)
        # Disallow any other class
        raise pickle.UnpicklingError(f"Disallowed pickled object: {module}.{name}")


def restricted_loads(data: bytes) -> Any:
    """Load pickled data using RestrictedUnpickler."""
    return RestrictedUnpickler(io.BytesIO(data)).load()


# ------------------------------------------------------------------
# Main conversion function
# ------------------------------------------------------------------
def convert_to_object(serialized_data: bytes, format_type: str) -> Any:
    """
    Convert serialized data back into a Python object.

    Parameters
    ----------
    serialized_data : bytes
        The serialized object in byte form.
    format_type : str
        One of the permitted serialized data formats: 'json', 'xml', 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If an untrusted or unsupported format_type is supplied.
    """
    allowed_formats = {'json', 'xml', 'pickle'}

    if format_type not in allowed_formats:
        raise ValueError(f"Untrusted or unsupported format: {format_type}")

    if format_type == 'json':
        # json.loads expects a str, so decode bytes using UTF-8
        return json.loads(serialized_data.decode('utf-8'))

    if format_type == 'xml':
        # Parse XML and convert to a nested dict structure
        root = ET.fromstring(serialized_data.decode('utf-8'))

        def _element_to_dict(elem):
            d = {elem.tag: {} if elem.attrib else None}
            children = list(elem)
            if children:
                dd = {}
                for child in children:
                    dd.update(_element_to_dict(child))
                d[elem.tag] = dd
            if elem.attrib:
                d[elem.tag].update(('@' + k, v) for k, v in elem.attrib.items())
            if elem.text and elem.text.strip():
                text = elem.text.strip()
                if children or elem.attrib:
                    d[elem.tag]['#text'] = text
                else:
                    d[elem.tag] = text
            return d

        return _element_to_dict(root)

    if format_type == 'pickle':
        # Use restricted unpickler to mitigate security risk
        return restricted_loads(serialized_data)

    # The function should never reach here due to the format check above
    raise ValueError("Unhandled format_type")


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     # JSON example
#     obj = {"foo": [1, 2, 3], "bar": True}
#     data = json.dumps(obj).encode('utf-8')
#     print(convert_to_object(data, 'json'))
#
#     # XML example
#     xml_data = b'<root><item>value</item></root>'
#     print(convert_to_object(xml_data, 'xml'))
#
#     # Pickle example
#     import io
#     pickled = pickle.dumps(obj)
#     print(convert_to_object(pickled, 'pickle'))