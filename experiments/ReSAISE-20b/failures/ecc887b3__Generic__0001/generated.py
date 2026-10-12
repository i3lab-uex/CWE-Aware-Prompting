import json
import xml.etree.ElementTree as ET

# Define the set of formats that are considered safe.
SAFE_FORMATS = {"json", "xml"}

def safe_deserialize(serialized_bytes: bytes, allowed_format: str):
    """
    Safely deserialize `serialized_bytes` according to the specified format.

    Parameters
    ----------
    serialized_bytes : bytes
        Raw byte representation of the serialized data.
    allowed_format : str
        The serialization format used ('json' or 'xml').

    Returns
    -------
    object
        The deserialized Python object. For JSON, this will be a native
        Python data structure (dict/list/etc.).  For XML, an `ElementTree.Element`
        instance is returned.

    Raises
    ------
    ValueError
        If `allowed_format` is not in the set of permitted formats.
    """
    fmt = allowed_format.lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format}")

    # Convert bytes to a string using UTF-8.
    try:
        text = serialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes are not valid UTF-8.") from exc

    if fmt == "json":
        # json.loads is safe for JSON data when used with default settings.
        return json.loads(text)

    if fmt == "xml":
        # ElementTree can parse XML strings.  It does not evaluate external
        # entities by default, but we disable DTD processing to avoid potential
        # attacks.
        parser = ET.XMLParser(resolve_entities=False, load_dtd=False)
        return ET.fromstring(text, parser=parser)

    # The check above ensures we never reach this point.
    raise AssertionError("Unhandled format encountered.")