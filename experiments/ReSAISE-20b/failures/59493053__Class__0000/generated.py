import json
from typing import Any

# We use defusedxml to safely parse XML and avoid XXE attacks.
try:
    from defusedxml import ElementTree as ET
except ImportError:  # pragma: no cover
    # If defusedxml is not available, fall back to the standard library
    # but warn that XML handling may be unsafe.
    import xml.etree.ElementTree as ET
    import warnings
    warnings.warn(
        "defusedxml is not installed; XML parsing may be vulnerable to XXE attacks."
    )


def deserialize_data(input_data: bytes, serialization_format: str) -> Any:
    """
    Deserialize a byte string into a Python object safely.

    Parameters
    ----------
    input_data : bytes
        The serialized data.
    serialization_format : str
        One of 'json', 'xml' or other supported formats.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered unsafe.
    """
    fmt = serialization_format.lower()

    if fmt == "json":
        # json.loads can handle bytes directly in Python 3.6+
        try:
            return json.loads(input_data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "xml":
        # Use defusedxml to avoid XXE and other XML-related attacks.
        try:
            root = ET.fromstring(input_data)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

        # Convert the ElementTree to a dictionary for easier consumption.
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

    # Disallow pickle or any other format that can execute code
    if fmt in {"pickle", "cPickle"}:
        raise ValueError(f"Deserialization of format '{serialization_format}' is prohibited for security reasons")

    # Any other formats are unsupported
    raise ValueError(f"Unsupported serialization format: {serialization_format}")