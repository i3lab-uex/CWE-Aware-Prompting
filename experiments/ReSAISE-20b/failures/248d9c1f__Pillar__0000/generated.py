import json
import xml.etree.ElementTree as ET
from typing import Any

# Allowed serialization formats.  Each format maps to a safe deserializer.
_TRUSTED_DESERIALIZERS = {
    "json": json.loads,
    # XML is parsed into an ElementTree.Element.  The caller can decide how to
    # use it, but we do not expose any executable code paths.
    "xml": ET.fromstring,
}

def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object using only trusted formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized data in binary form.
    encoding_type : str
        The serialization format ('json', 'xml').

    Returns
    -------
    Any
        The deserialized Python object.  For JSON it will be a dict/list/etc.
        For XML it will be an `xml.etree.ElementTree.Element`.

    Raises
    ------
    ValueError
        If the requested format is not in the whitelist of trusted formats,
        or if deserialization fails due to malformed input.
    """
    # Normalise the format name (case‑insensitive) and look up the deserializer.
    fmt = encoding_type.strip().lower()
    if fmt not in _TRUSTED_DESERIALIZERS:
        raise ValueError(f"Unsupported or unsafe format '{encoding_type}'. "
                         f"Allowed formats: {', '.join(_TRUSTED_DESERIALIZERS)}")

    deserializer = _TRUSTED_DESERIALIZERS[fmt]

    # Decode bytes to string for text‑based formats.
    try:
        if fmt in ("json", "xml"):
            # Assume UTF‑8 encoding for text formats.
            text = byte_data.decode("utf-8")
        else:
            # Should never reach here due to whitelist.
            raise ValueError(f"Unhandled format: {encoding_type}")
    except Exception as exc:
        raise ValueError(f"Failed to decode byte data: {exc}") from exc

    # Perform deserialization.  Any exception is wrapped as ValueError to
    # provide a consistent error type for callers.
    try:
        return deserializer(text)
    except Exception as exc:
        raise ValueError(f"Deserialization error for format '{encoding_type}': {exc}") from exc