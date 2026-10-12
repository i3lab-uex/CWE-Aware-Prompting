import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# Registry of allowed serialization methods.
ALLOWED_METHODS = {
    'json': 'JSON',
    'csv': 'CSV'
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from the given byte stream using the specified method.

    Parameters
    ----------
    serialized_bytes : bytes
        The data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unrecognized or insecure.
    """
    # Normalize method name to lower case
    method = serialization_method.lower()

    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: '{serialization_method}'")

    # JSON deserialization
    if method == 'json':
        try:
            text = serialized_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    # CSV deserialization – returns a list of dictionaries
    if method == 'csv':
        try:
            # Use BytesIO to wrap the byte stream and TextIOWrapper for text decoding
            with BytesIO(serialized_bytes) as bio:
                with TextIOWrapper(bio, encoding='utf-8') as text_stream:
                    reader = csv.DictReader(text_stream)
                    return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to decode CSV data") from exc

    # Should never reach here due to the registry check
    raise ValueError(f"Unhandled serialization method: '{serialization_method}'")