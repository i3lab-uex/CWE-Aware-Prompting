import json
from typing import Any

# For safe XML parsing we use defusedxml which mitigates XML External Entity attacks
try:
    from defusedxml.ElementTree import fromstring as safe_fromstring
except ImportError:
    # Fallback to standard ElementTree if defusedxml is not available,
    # but warn that XML parsing may be unsafe.
    import warnings
    from xml.etree.ElementTree import fromstring as safe_fromstring

    warnings.warn(
        "defusedxml is not installed. XML parsing may be unsafe.",
        RuntimeWarning,
    )

# Define the set of trusted formats
TRUSTED_FORMATS = {"json", "xml"}


def deserialize_data(input_data: bytes, data_type: str) -> Any:
    """
    Deserialize raw bytes into a Python object using only trusted formats.

    Parameters
    ----------
    input_data : bytes
        Serialized data in byte format.
    data_type : str
        The serialization format. Supported values are 'json' and 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the provided data_type is not in TRUSTED_FORMATS or if deserialization fails.
    """
    fmt = data_type.lower()
    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe data type: {data_type!r}")

    try:
        if fmt == "json":
            # JSON is safe; decode bytes to string first
            text = input_data.decode("utf-8")
            return json.loads(text)

        if fmt == "xml":
            # Parse XML safely using defusedxml
            root = safe_fromstring(input_data)
            return _xml_to_dict(root)

    except Exception as exc:
        # Wrap any parsing exception in a ValueError to avoid leaking details
        raise ValueError(f"Failed to deserialize data as {data_type}") from exc


def _xml_to_dict(element) -> Any:
    """
    Convert an ElementTree element into a nested dictionary.
    Handles attributes and child elements recursively.
    """
    def recurse(elem):
        # Element's text content
        data = elem.text.strip() if elem.text and elem.text.strip() else None

        # Process child elements
        children = list(elem)
        if children:
            child_dict = {}
            for child in children:
                child_obj = recurse(child)
                tag = child.tag
                # Handle multiple occurrences of the same tag
                if tag in child_dict:
                    if not isinstance(child_dict[tag], list):
                        child_dict[tag] = [child_dict[tag]]
                    child_dict[tag].append(child_obj)
                else:
                    child_dict[tag] = child_obj
            # Merge attributes and children
            result = {"@attributes": elem.attrib} if elem.attrib else {}
            result.update(child_dict)
            if data:
                result["#text"] = data
            return result

        # No children: return attributes + text if present
        if elem.attrib:
            result = {"@attributes": elem.attrib}
            if data:
                result["#text"] = data
            return result

        # Leaf node with only text
        return data if data is not None else ""

    return {element.tag: recurse(element)}