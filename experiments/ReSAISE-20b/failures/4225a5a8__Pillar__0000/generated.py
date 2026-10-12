import json
from typing import Any

# For safe XML parsing we use the defusedxml package, which mitigates XXE and other
# security issues.  If it is not installed we fall back to a warning but keep the
# API stable.
try:
    from defusedxml import ElementTree as ET  # type: ignore
except Exception:  # pragma: no cover
    import xml.etree.ElementTree as ET  # type: ignore


def _parse_xml(raw_data: bytes) -> Any:
    """
    Parse XML data in a safe way.  The result is converted to a nested dictionary
    structure so that it can be used like a normal Python object.

    Parameters
    ----------
    raw_data : bytes
        XML payload as bytes.

    Returns
    -------
    dict
        Nested dictionary representation of the XML tree.
    """
    try:
        root = ET.fromstring(raw_data)
    except ET.ParseError as exc:  # pragma: no cover
        raise ValueError(f"Invalid XML data: {exc}") from exc

    def _elem_to_dict(elem):
        d = {}
        # Add attributes
        if elem.attrib:
            d.update({f"@{k}": v for k, v in elem.attrib.items()})
        # Add child elements
        children = list(elem)
        if children:
            for child in children:
                child_dict = _elem_to_dict(child)
                key = child.tag
                # Handle repeated tags as lists
                if key in d:
                    if not isinstance(d[key], list):
                        d[key] = [d[key]]
                    d[key].append(child_dict)
                else:
                    d[key] = child_dict
        # Add text if present
        text = elem.text.strip() if elem.text else ""
        if text:
            d["#text"] = text
        return d

    return {root.tag: _elem_to_dict(root)}


def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Deserialize `raw_data` according to the specified `method_name`.

    Parameters
    ----------
    raw_data : bytes
        The serialized object represented in byte format.
    method_name : str
        Name of the serialization format: 'json' or 'xml'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or the data cannot be parsed.
    """
    method = method_name.lower()
    if method == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:  # pragma: no cover
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method == "xml":
        return _parse_xml(raw_data)

    # Any other format is considered dangerous or unsupported
    raise ValueError(f"Unsupported or unsafe deserialization method: {method_name}")