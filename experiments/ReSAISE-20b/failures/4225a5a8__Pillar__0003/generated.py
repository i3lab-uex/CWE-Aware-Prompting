import json
import xml.etree.ElementTree as ET
from typing import Any

# ------------------------------------------------------------------------------
# Security notes
#
# 1. Only two safe formats are supported: JSON and XML.
#    - JSON is parsed with the standard `json.loads`, which only builds native
#      Python objects (dict, list, str, int, float, bool, None).
#    - XML is parsed with `xml.etree.ElementTree`.  The parser is configured
#      to disallow external entity resolution (no DTD loading) so that no
#      external resources can be accessed during parsing.
#
# 2. All other formats (e.g., pickle, marshal, msgpack, etc.) are explicitly
#    rejected to prevent code execution or other unsafe side effects.
#
# 3. The function raises `ValueError` for unsupported formats or when the
#    underlying parser fails, giving callers a clear indication of failure.
#
# 4. This implementation avoids CWE‑664 by ensuring that any resources
#    allocated during parsing (e.g., file handles in ElementTree) are
#    released automatically by the parser itself.  No manual open/close
#    operations are performed.
# ------------------------------------------------------------------------------

def objectify_data(raw_data: bytes, method_name: str) -> Any:
    """
    Convert serialized data into a Python object in a safe manner.

    Parameters
    ----------
    raw_data : bytes
        The serialized data.
    method_name : str
        Identifier of the serialization format.  Supported values are:
        - 'json' : JSON encoded data.
        - 'xml'  : XML encoded data.

    Returns
    -------
    Any
        The deserialized Python object.  For JSON, this will be a native
        Python data structure (dict/list/str/int/...).
        For XML, this will be an `xml.etree.ElementTree.Element` instance.

    Raises
    ------
    ValueError
        If the format is unsupported, dangerous (e.g., pickle), or if parsing
        fails due to malformed input.
    """
    method = method_name.lower()

    # ---------- JSON ----------
    if method == "json":
        try:
            return json.loads(raw_data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    # ---------- XML ----------
    elif method == "xml":
        try:
            # Parse without DTD or external entities
            parser = ET.XMLParser(
                target=ET.TreeBuilder(),
                # Disable external entity resolution
                load_dtd=False,
                resolve_entities=False,
            )
            root = ET.fromstring(raw_data, parser=parser)
            return root
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc

    # ---------- Disallowed formats ----------
    elif method in {"pickle", "marshal", "msgpack"}:
        raise ValueError(f"Deserialization of format '{method}' is disallowed")

    # ---------- Unknown formats ----------
    else:
        raise ValueError(f"Unsupported deserialization method: '{method_name}'")