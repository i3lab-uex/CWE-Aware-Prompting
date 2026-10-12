import json
from typing import Any

# Import the safe XML parser from defusedxml.
# This library mitigates XML-based attacks (e.g., XXE, DoS).
try:
    from defusedxml import ElementTree as ET
except ImportError as exc:
    raise RuntimeError(
        "The `defusedxml` package is required for safe XML deserialization. "
        "Install it via pip: `pip install defusedxml`"
    ) from exc

# Define the set of formats that are considered safe for deserialization.
SAFE_FORMATS = {"json", "xml"}

def _parse_json(data: bytes) -> Any:
    """Parse JSON data safely."""
    # json.loads accepts a string; decode using UTF-8.
    return json.loads(data.decode("utf-8"))

def _parse_xml(data: bytes) -> Any:
    """Parse XML data safely using defusedxml."""
    # Parse the XML into an ElementTree.
    root = ET.fromstring(data)
    # Convert the ElementTree to a nested dictionary for easier use.
    def elem_to_dict(elem):
        d = {elem.tag: {} if elem.attrib else None}
        children = list(elem)
        if children:
            dd = {}
            for child in children:
                child_dict = elem_to_dict(child)
                dd.update(child_dict)
            d[elem.tag] = dd
        if elem.attrib:
            d[elem.tag].update(("@" + k, v) for k, v in elem.attrib.items())
        if elem.text and elem.text.strip():
            d[elem.tag]["#text"] = elem.text.strip()
        return d
    return elem_to_dict(root)

def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize data from a known and trusted format.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte representation of the serialized object.
    allowed_format : str
        The format used for serialization. Supported values are:
        - 'json'
        - 'xml'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is not in the set of safe formats.
    """
    fmt = allowed_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{allowed_format}'. "
            f"Allowed formats: {', '.join(sorted(SAFE_FORMATS))}"
        )

    if fmt == "json":
        return _parse_json(serialized_bytes)
    elif fmt == "xml":
        return _parse_xml(serialized_bytes)

    # This point should never be reached because of the validation above.
    raise ValueError(f"Unhandled format: {allowed_format}")