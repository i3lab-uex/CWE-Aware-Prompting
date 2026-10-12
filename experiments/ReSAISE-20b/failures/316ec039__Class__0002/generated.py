import json
import csv
from io import StringIO

# List of trusted serialization formats
TRUSTED_METHODS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str):
    """
    Restore a Python object from serialized data using only trusted methods.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    deserialization_method : str
        The name of the serialization format ('json' or 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in TRUSTED_METHODS or if deserialization fails.
    """
    method = deserialization_method.lower()
    if method not in TRUSTED_METHODS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")

    try:
        if method == "json":
            # json.loads expects a str, so decode bytes using utf-8
            return json.loads(serialized_data.decode("utf-8"))
        elif method == "csv":
            # csv.DictReader returns an iterator of dicts; convert to list
            text = serialized_data.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]
    except Exception as exc:
        # Wrap any underlying exception into ValueError to keep the API consistent
        raise ValueError(f"Failed to deserialize data with method '{deserialization_method}': {exc}") from exc