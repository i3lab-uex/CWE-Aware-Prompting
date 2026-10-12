import json
import xml.etree.ElementTree as ET
from typing import Any

def deserialize_data(input_data: bytes, serialization_format: str) -> Any:
    """
    Safely deserializes data from a supported format.

    Parameters
    ----------
    input_data : bytes
        The serialized object in byte form.
    serialization_format : str
        One of the supported formats: 'json', 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or if deserialization fails.
    """
    fmt = serialization_format.lower()
    try:
        if fmt == 'json':
            # JSON is safe by default; decode bytes to str using utf-8
            text = input_data.decode('utf-8')
            return json.loads(text)

        elif fmt == 'xml':
            # ElementTree is limited in what it can construct; avoid external entities
            # Parse the XML string and convert to a simple dictionary representation.
            text = input_data.decode('utf-8')
            root = ET.fromstring(text)

            def _elem_to_dict(elem):
                d = {}
                # Attributes
                if elem.attrib:
                    d.update({f"@{k}": v for k, v in elem.attrib.items()})
                # Children
                children = list(elem)
                if children:
                    child_dict = {}
                    for child in children:
                        child_entry = _elem_to_dict(child)
                        if child.tag in child_dict:
                            # If tag already exists, make it a list
                            if not isinstance(child_dict[child.tag], list):
                                child_dict[child.tag] = [child_dict[child.tag]]
                            child_dict[child.tag].append(child_entry)
                        else:
                            child_dict[child.tag] = child_entry
                    d.update(child_dict)
                # Text content
                text_content = elem.text.strip() if elem.text else ''
                if text_content and not children:
                    d['#text'] = text_content
                return d

            return {root.tag: _elem_to_dict(root)}

        else:
            raise ValueError(f"Unsupported serialization format: {serialization_format}")

    except (json.JSONDecodeError, ET.ParseError, UnicodeDecodeError) as exc:
        raise ValueError(f"Deserialization failed for format '{serialization_format}': {exc}") from exc