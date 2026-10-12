import json
import csv
from io import BytesIO, TextIOWrapper

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str):
    """
    Safely reconstruct a Python object from serialized byte data.

    Parameters
    ----------
    deserialized_bytes : bytes
        The raw byte stream containing the serialized data.
    method_for_serialization : str
        Identifier of the serialization format. Supported values are:
            - 'json'
            - 'csv'

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    # Define a whitelist of safe serialization formats
    _SAFE_METHODS = {
        'json': _deserialize_json,
        'csv' : _deserialize_csv
    }

    method = method_for_serialization.lower()
    if method not in _SAFE_METHODS:
        raise ValueError(f"Unsupported or unsafe serialization method: {method}")

    # Delegate to the appropriate deserializer
    return _SAFE_METHODS[method](deserialized_bytes)

# --------------------------------------------------------------------------- #
# Internal helper functions
def _deserialize_json(data: bytes):
    """Deserialize JSON data safely."""
    try:
        text = data.decode('utf-8')
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Failed to decode JSON data") from exc

def _deserialize_csv(data: bytes):
    """
    Deserialize CSV data into a list of dictionaries.
    Each row is represented as a dict mapping column names to values.
    """
    try:
        buffer = BytesIO(data)
        # TextIOWrapper handles decoding; newline='' ensures universal newlines
        text_wrapper = TextIOWrapper(buffer, encoding='utf-8', newline='')
        reader = csv.DictReader(text_wrapper)
        return list(reader)
    except Exception as exc:
        raise ValueError("Failed to decode CSV data") from exc