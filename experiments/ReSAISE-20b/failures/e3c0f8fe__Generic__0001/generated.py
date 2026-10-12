import json
import csv
from io import BytesIO, TextIOWrapper

# Registry of allowed serialization methods and their handlers
_ALLOWED_METHODS = {
    "json": lambda b: json.loads(b.decode("utf-8")),
    # CSV will be handled specially below
}


def _deserialize_csv(b: bytes):
    """
    Deserialize CSV data into a list of dictionaries.
    Each row is represented as a dict mapping column names to values.
    """
    with BytesIO(b) as buffer:
        # TextIOWrapper allows csv module to read strings
        with TextIOWrapper(buffer, encoding="utf-8") as text:
            reader = csv.DictReader(text)
            return [row for row in reader]


def restore_object(serialized_bytes: bytes, serialization_method: str):
    """
    Restore a Python object from serialized data.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte stream containing the serialized data.
    serialization_method : str
        Identifier of the serialization format. Must be one of the
        allowed methods ('json', 'csv').

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
    if method == "csv":
        return _deserialize_csv(serialized_bytes)

    handler = _ALLOWED_METHODS.get(method)
    if handler is None:
        raise ValueError(f"Unsupported or insecure serialization method: {serialization_method}")

    return handler(serialized_bytes)