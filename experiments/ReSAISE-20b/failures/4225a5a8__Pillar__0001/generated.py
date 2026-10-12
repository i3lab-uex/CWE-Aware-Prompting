import json
from typing import Any

# We use the defusedxml library to safely parse XML without external entity expansion.
# If it's not available, we fall back to the standard library with a custom parser that disables external entities.
try:
    from defusedxml.ElementTree import XML
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as ET

    def XML(data: bytes):
        # Disable external entities by not loading any DTD
        parser = ET.XMLParser(resolve_entities=False)
        return ET.fromstring(data, parser=parser)


def _parse_json(raw_data: bytes) -> Any:
    """Parse JSON data safely."""
    try:
        text = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON data is not valid UTF-8") from exc
    return json.loads(text)


def _parse_xml(raw_data: bytes) -> Any:
    """Parse XML data safely and convert it to a dictionary."""
    try:
        root = XML(raw_data)
    except Exception as exc:  # pragma: no cover
        raise ValueError("Invalid XML data") from exc

    def _element_to_dict(elem):
        d = {elem.tag: {} if elem.attrib else None}
        children = list(elem)
        if children:
            dd = {}
            for child in children:
                dd.update(_element_to_dict(child))
            d[elem.tag] = dd
        if elem.attrib:
            d[elem.tag].update(("@" + k, v) for k, v in elem.attrib.items())
        text = (elem.text or "").strip()
        if text:
            d[elem.tag]["#text"] = text
        return d

    return _element_to_dict(root)


def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize *raw_data* according to the specified *method_name*.

    Supported formats:
        - 'json' : JSON text encoded in UTF‑8
        - 'xml'  : XML data parsed with a safe parser

    Any other format will raise ValueError.

    Parameters
    ----------
    raw_data : bytes
        Serialized data in byte form.
    method_name : str
        Name of the serialization format ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or deserialization fails.
    """
    method = method_name.lower()
    if method == "json":
        return _parse_json(raw_data)
    elif method == "xml":
        return _parse_xml(raw_data)
    else:
        raise ValueError(f"Unsupported or dangerous format: {method_name!r}")