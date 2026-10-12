import json
import xml.etree.ElementTree as ET
from typing import Any


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize `byte_data` into a Python object according to the specified
    serialization format. Only safe, trusted formats are supported.

    Parameters:
        byte_data (bytes): The serialized data in bytes.
        encoding_type (str): The serialization format ('json' or 'xml').

    Returns:
        Any: The deserialized Python object. For JSON it returns a dict/list/etc.
             For XML it returns an ElementTree.Element representing the root.

    Raises:
        ValueError: If `encoding_type` is not supported or if deserialization fails.
    """
    # Define the set of trusted formats
    TRUSTED_FORMATS = {"json", "xml"}

    if encoding_type not in TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe format '{encoding_type}'. "
            f"Only the following formats are allowed: {', '.join(TRUSTED_FORMATS)}."
        )

    try:
        if encoding_type == "json":
            # JSON is text based; decode using UTF-8
            text = byte_data.decode("utf-8")
            return json.loads(text)

        if encoding_type == "xml":
            # XML is also text based; decode using UTF-8
            text = byte_data.decode("utf-8")
            # Parse into an ElementTree.Element; this is safe and does not
            # evaluate any embedded code.
            return ET.fromstring(text)

    except (UnicodeDecodeError, json.JSONDecodeError, ET.ParseError) as exc:
        raise ValueError(f"Failed to deserialize data: {exc}") from exc