import json
import xml.etree.ElementTree as ET

def deserialize_data(input_data: bytes, data_type: str):
    """
    Deserialize raw byte data into a Python object using only
    trusted serialization formats.

    Parameters
    ----------
    input_data : bytes
        The serialized data in byte form.
    data_type : str
        One of the supported formats: 'json', 'xml'.

    Returns
    -------
    object
        The deserialized Python representation.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous format is requested.
    """
    # Map supported types to deserialization functions
    if data_type.lower() == 'json':
        try:
            text = input_data.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON data: {exc}") from exc

    if data_type.lower() == 'xml':
        try:
            text = input_data.decode('utf-8')
            # ElementTree is used here; it parses XML into an Element tree.
            return ET.fromstring(text)
        except (UnicodeDecodeError, ET.ParseError) as exc:
            raise ValueError(f"Failed to deserialize XML data: {exc}") from exc

    # Reject any other format (e.g., pickle, marshal) to avoid security risks
    raise ValueError(f"Unsupported or dangerous data_type: '{data_type}'. "
                     "Allowed types are 'json' and 'xml'.")