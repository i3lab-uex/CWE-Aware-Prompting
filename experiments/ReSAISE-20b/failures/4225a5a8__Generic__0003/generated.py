import json
from xml.etree import ElementTree as ET


def objectify_data(raw_data: bytes, method_name: str):
    """
    Safely deserialize serialized data into a Python object.

    Parameters
    ----------
    raw_data : bytes
        The serialized representation of the data.
    method_name : str
        One of 'json', 'xml'.  The function explicitly rejects other formats.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method_name is unsupported or potentially unsafe.
    """
    if not isinstance(raw_data, bytes):
        raise TypeError("raw_data must be of type 'bytes'")

    method_name = method_name.lower()

    if method_name == "json":
        # JSON is safe; decode bytes and parse
        try:
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 encoding for JSON data") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Malformed JSON data") from exc

    elif method_name == "xml":
        # XML parsing with ElementTree is safe as long as we avoid external entities.
        try:
            root = ET.fromstring(raw_data)
        except ET.ParseError as exc:
            raise ValueError("Malformed XML data") from exc

        # Convert the ElementTree to a Python dict for easier use.
        def _elem_to_dict(elem):
            d = {elem.tag: {} if elem.attrib else None}
            children = list(elem)
            if children:
                dd = {}
                for child in children:
                    dd.update(_elem_to_dict(child))
                d[elem.tag] = dd
            if elem.attrib:
                d[elem.tag].update({f"@{k}": v for k, v in elem.attrib.items()})
            text = elem.text.strip() if elem.text else None
            if text:
                d[elem.tag]["#text"] = text
            return d

        return _elem_to_dict(root)

    else:
        # Explicitly reject potentially dangerous formats such as pickle.
        raise ValueError(f"Unsupported or unsafe deserialization method: {method_name}")