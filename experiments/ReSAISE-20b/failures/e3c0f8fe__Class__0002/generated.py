import json
import csv
from io import StringIO
from typing import Any

# Registry of allowed serialization methods
ALLOWED_METHODS = {
    "json": json.loads,
    # CSV will be handled specially
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
        If the method is unrecognized, insecure, or not supported.
    """
    method = serialization_method.lower()

    if method == "csv":
        # CSV is treated as a list of dictionaries
        text = serialized_bytes.decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    loader = ALLOWED_METHODS[method]
    return loader(serialized_bytes.decode("utf-8"))