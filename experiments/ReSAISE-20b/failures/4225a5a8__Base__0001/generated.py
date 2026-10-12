import json
import xml.etree.ElementTree as ET

def objectify_data(raw_data: bytes, method_name: str):
    """
    Deserialize `raw_data` into a Python object using the specified format.

    Supported formats:
        - 'json': JSON text encoded in UTF-8
        - 'xml' : Simple XML representation (converted to nested dict)

    Any other format raises ValueError.

    Parameters
    ----------
    raw_data : bytes
        Serialized data in byte form.
    method_name : str
        The name of the serialization format ('json', 'xml').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or dangerous.
    """
    if not isinstance(raw_data, bytes):
        raise ValueError("raw_data must be bytes")

    method_name = method_name.lower()

    if method_name == "json":
        try:
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    if method_name == "xml":
        try:
            root = ET.fromstring(raw_data)
        except ET.ParseError as exc:
            raise ValueError("Malformed XML data") from exc

        def elem_to_dict(elem):
            d = {elem.tag: {} if elem.attrib else None}
            children = list(elem)
            if children:
                child_dicts = [elem_to_dict(child) for child in children]
                d[elem.tag] = {k: v for child in child_dicts for k, v in child.items()}
            if elem.attrib:
                d[elem.tag].update({f"@{k}": v for k, v in elem.attrib.items()})
            text = elem.text.strip() if elem.text else None
            if text:
                d[elem.tag]["#text"] = text
            return d

        return elem_to_dict(root)

    # Disallow pickle or any other format
    raise ValueError(f"Unsupported or dangerous deserialization format: {method_name}")