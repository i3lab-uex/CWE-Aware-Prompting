import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Registry of allowed serialization methods
ALLOWED_METHODS = {
    'json': json.loads,
    # csv is handled specially because it returns a list of dictionaries
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from the given byte stream using the specified method.

    Parameters
    ----------
    serialized_bytes : bytes
        The data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not recognized or insecure.
    """
    method = serialization_method.lower()

    if method == 'json':
        try:
            text = serialized_bytes.decode('utf-8')
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Failed to decode JSON data: {exc}") from exc

    if method == 'csv':
        try:
            text = serialized_bytes.decode('utf-8')
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError(f"Failed to decode CSV data: {exc}") from exc

    # Disallow any other methods (including pickle, marshal, etc.)
    raise ValueError(f"Unrecognized or insecure serialization method: '{serialization_method}'")