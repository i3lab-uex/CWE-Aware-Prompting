import json
from typing import Any

# Use defusedxml to safely parse XML and avoid XXE attacks.
try:
    from defusedxml import ElementTree as ET
except ImportError:
    # If defusedxml is not available, fall back to the standard library
    # but note that this may be less secure.
    import xml.etree.ElementTree as ET


ALLOWED_METHODS = {"json", "xml"}

def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Deserialize `encoded_data` using the specified `method`.

    Parameters
    ----------
    encoded_data : bytes
        The serialized data in byte form.
    method : str
        One of the supported formats: 'json', 'xml'.
        'pickle' is intentionally disallowed for security reasons.

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the method is not supported or unsafe.
    """
    if method.lower() not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or dangerous serialization format: {method}")

    try:
        if method.lower() == "json":
            # Decode bytes to string using UTF-8; errors='strict' will raise on invalid data.
            text = encoded_data.decode("utf-8", errors="strict")
            return json.loads(text)

        elif method.lower() == "xml":
            # Use defusedxml for secure XML parsing.
            text = encoded_data.decode("utf-8", errors="strict")
            return ET.fromstring(text)

    except Exception as exc:
        # Wrap any parsing errors in a ValueError for consistency.
        raise ValueError(f"Failed to deserialize data with method '{method}': {exc}") from exc