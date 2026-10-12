import json
import xml.etree.ElementTree as ET
from typing import Any


def data_to_object(byte_data: bytes, encoding_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object using only safe, trusted formats.

    Parameters
    ----------
    byte_data : bytes
        The serialized object in byte format.
    encoding_type : str
        The serialization format. Supported values are:
            - 'json'
            - 'xml'

    Returns
    -------
    Any
        The deserialized Python object. For JSON it is a standard Python data structure.
        For XML it returns an ``xml.etree.ElementTree.Element`` representing the root.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    # Define the set of trusted formats
    TRUSTED_FORMATS = {"json", "xml"}

    # Normalise the requested format
    fmt = encoding_type.lower()

    if fmt not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {encoding_type!r}")

    # Decode the bytes safely; UTF-8 is a common default for text formats
    try:
        text = byte_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data could not be decoded as UTF-8") from exc

    if fmt == "json":
        # Use json.loads which only produces basic Python data structures
        return json.loads(text)

    if fmt == "xml":
        # Parse XML using ElementTree.  The parser is safe against common
        # XML vulnerabilities (e.g., no external entity resolution).
        try:
            return ET.fromstring(text)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML data") from exc