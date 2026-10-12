import json
import csv
import io
from typing import Any

# Registry of trusted serialization methods
ALLOWED_METHODS = {
    "json": "JSON",
    "csv": "CSV",
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize data from a trusted format.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw data to deserialize.
    serialization_method : str
        Identifier of the serialization format ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unknown or insecure.
    """
    method = serialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    if method == "json":
        # json.loads accepts str, so decode bytes first
        return json.loads(serialized_bytes.decode("utf-8"))

    if method == "csv":
        # Use csv.DictReader to convert CSV rows into dictionaries
        with io.StringIO(serialized_bytes.decode("utf-8")) as f:
            reader = csv.DictReader(f)
            return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {serialization_method}")