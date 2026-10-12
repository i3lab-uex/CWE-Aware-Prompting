import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, serialization_format: str):
    """
    Safely deserialize data from a trusted set of formats.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte format.
    serialization_format : str
        Format used for serialization. Only 'json' and 'xml'
        are allowed.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered dangerous.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        # Decode bytes to string, then load JSON
        try:
            text = input_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    elif fmt == "xml":
        # Parse XML safely without external entities
        try:
            root = ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError("Malformed XML data") from exc

        # Convert ElementTree to a dictionary representation
        def elem_to_dict(elem):
            d = {elem.tag: {} if elem.attrib else None}
            children = list(elem)
            if children:
                dd = {}
                for child in children:
                    dd.update(elem_to_dict(child))
                d[elem.tag] = dd
            if elem.attrib:
                d[elem.tag].update({f"@{k}": v for k, v in elem.attrib.items()})
            if elem.text and elem.text.strip():
                d[elem.tag]["#text"] = elem.text.strip()
            return d

        return elem_to_dict(root)

    else:
        # Disallow all other formats (e.g., pickle, marshal, etc.)
        raise ValueError(f"Unsupported or dangerous serialization format: {serialization_format}")