import json
from typing import Any

# Use a safe XML parser that protects against XXE and other attacks.
try:
    from defusedxml import ElementTree as ET
except ImportError:
    # Fallback to standard library if defusedxml is not available.
    # Note: this fallback is NOT recommended for production use.
    import xml.etree.ElementTree as ET

def decode_serialized_data(encoded_data: bytes, method: str) -> Any:
    """
    Safely deserialize data from a known and trusted format.

    Parameters
    ----------
    encoded_data : bytes
        The serialized object represented in byte format.
    method : str
        Serialization format used: 'json', 'xml', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or potentially dangerous.
    """
    method = method.lower()

    if method == "json":
        # JSON is safe as it only represents basic data types.
        try:
            text = encoded_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON deserialization") from exc
        return json.loads(text)

    if method == "xml":
        # Use a safe XML parser that prevents XXE and other attacks.
        try:
            return ET.fromstring(encoded_data)
        except ET.ParseError as exc:
            raise ValueError("Failed to parse XML") from exc

    # Pickle is explicitly disallowed because it can execute arbitrary code.
    if method == "pickle":
        raise ValueError("Deserialization of pickle data is forbidden for security reasons")

    # Any other method is unsupported.
    raise ValueError(f"Unsupported serialization format: {method}")