import json
import xml.etree.ElementTree as ET

# List of permitted, safe data formats
ALLOWED_FORMATS = {"json", "xml"}

def load_serialized_data(bytes_data: bytes, data_format: str):
    """
    Safely deserialize `bytes_data` according to the specified `data_format`.

    Parameters
    ----------
    bytes_data : bytes
        The raw serialized data.
    data_format : str
        Identifier of the serialization format. Supported values are
        "json" and "xml".

    Returns
    -------
    object
        The Python representation of the deserialized data.

    Raises
    ------
    ValueError
        If `data_format` is not in the list of allowed formats.
    json.JSONDecodeError, ET.ParseError
        Propagated if the underlying parser fails.
    """
    fmt = data_format.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or unsafe format: {data_format!r}")

    if fmt == "json":
        # JSON is safe for deserialization when using json.loads
        return json.loads(bytes_data.decode("utf-8"))

    if fmt == "xml":
        # Parse XML into an ElementTree element. The caller can convert it to
        # a dictionary or other structure if desired.
        return ET.fromstring(bytes_data.decode("utf-8"))

    # This line is theoretically unreachable due to the check above,
    # but it satisfies static type checkers.
    raise ValueError(f"Unhandled format: {data_format!r}")