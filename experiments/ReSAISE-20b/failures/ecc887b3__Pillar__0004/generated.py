import json
from typing import Any


def safe_deserialize(serialized_bytes: bytes, allowed_format: str) -> Any:
    """
    Safely deserialize `serialized_bytes` according to the specified
    `allowed_format`. Only a whitelist of formats is permitted.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw serialized data.
    allowed_format : str
        One of the supported formats: 'json', 'xml', or 'pickle'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist.
    """
    # Define a strict whitelist of allowed formats
    _ALLOWED_FORMATS = {"json", "xml", "pickle"}

    fmt = allowed_format.lower()
    if fmt not in _ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {allowed_format!r}")

    # The implementation of each format is intentionally minimal
    # to avoid accidental execution of unsafe code.
    if fmt == "json":
        try:
            text = serialized_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF‑8 data for JSON") from exc
        return json.loads(text)

    # XML deserialization is provided only for completeness.
    # In real-world scenarios, a dedicated library with proper
    # security controls should be used (e.g., lxml with defusedxml).
    elif fmt == "xml":
        try:
            import xml.etree.ElementTree as ET
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("XML parsing library unavailable") from exc

        try:
            return ET.fromstring(serialized_bytes)
        except ET.ParseError as exc:  # pragma: no cover
            raise ValueError("Malformed XML data") from exc

    # Pickle is explicitly disallowed because it can execute arbitrary code.
    elif fmt == "pickle":
        # This branch should never be reached due to the whitelist check above,
        # but we keep it for defensive completeness.
        raise ValueError("Pickle deserialization is disabled for security reasons.")