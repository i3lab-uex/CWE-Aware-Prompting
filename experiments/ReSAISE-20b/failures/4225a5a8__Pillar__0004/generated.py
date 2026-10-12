import json
import xml.etree.ElementTree as ET

def objectify_data(raw_data: bytes, method_name: str):
    """
    Deserialize `raw_data` according to the specified `method_name`.

    Supported formats: 'json', 'xml'.
    The 'pickle' format is explicitly disallowed to prevent arbitrary code execution.

    Parameters
    ----------
    raw_data : bytes
        Serialized data in byte format.
    method_name : str
        The name of the serialization format used ('json', 'xml' or other).

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported or considered dangerous.
    """
    if not isinstance(raw_data, bytes):
        raise ValueError("raw_data must be a bytes object")

    method = method_name.lower()

    if method == 'json':
        try:
            text = raw_data.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to deserialize JSON: {exc}") from exc

    if method == 'xml':
        try:
            # ElementTree parses XML safely; it does not execute code.
            return ET.fromstring(raw_data)
        except ET.ParseError as exc:
            raise ValueError(f"Failed to deserialize XML: {exc}") from exc

    if method == 'pickle':
        # Pickle is disallowed because it can execute arbitrary code.
        raise ValueError("Deserialization of pickle data is prohibited for security reasons")

    # Any other format is unsupported
    raise ValueError(f"Unsupported serialization method: {method_name}")