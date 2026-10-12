import json
import xml.etree.ElementTree as ET

# List of formats that are considered safe for deserialization
SAFE_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize *bytes_data* according to the specified *data_format*.

    Parameters
    ----------
    bytes_data : bytes
        The raw serialized data.
    data_format : str
        Identifier of the serialization format. Supported values are
        ``"json"``, and ``"xml"`` (case‑insensitive).

    Returns
    -------
    object
        The deserialized Python data structure. For JSON, a native Python
        object is returned (dict/list/etc.).  For XML, an :class:`ElementTree`
        element representing the root of the parsed XML tree is returned.

    Raises
    ------
    ValueError
        If *data_format* is not in :data:`SAFE_FORMATS` or if the data cannot
        be parsed for that format.
    """
    fmt = data_format.strip().lower()
    if fmt not in SAFE_FORMATS:
        raise ValueError(f"Unsupported or unsafe data format: {data_format!r}")

    try:
        if fmt == "json":
            # JSON expects a text string; decode using UTF‑8
            return json.loads(bytes_data.decode("utf-8"))
        elif fmt == "xml":
            # XML expects a text string; decode using UTF‑8
            return ET.fromstring(bytes_data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, ET.ParseError) as exc:
        raise ValueError(f"Failed to deserialize data for format {data_format!r}: {exc}") from exc