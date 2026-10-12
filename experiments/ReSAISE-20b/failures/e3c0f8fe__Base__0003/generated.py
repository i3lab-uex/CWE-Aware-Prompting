import json
import csv
import io
from typing import Any, Dict

# Registry of trusted serialization methods
ALLOWED_METHODS: Dict[str, str] = {
    "json": "json",
    "csv": "csv",
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Safely restore a Python object from serialized data.

    Parameters
    ----------
    serialized_bytes : bytes
        The binary data to deserialize.
    serialization_method : str
        Identifier of the serialization format. Supported values are
        "json" and "csv".

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not in the allowed list or if the data cannot be parsed.
    """
    # Ensure the method is recognized and safe
    method = ALLOWED_METHODS.get(serialization_method.lower())
    if not method:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    try:
        if method == "json":
            # json.loads expects a string; decode using utf-8
            return json.loads(serialized_bytes.decode("utf-8"))
        elif method == "csv":
            # CSV is read as text; decode and use csv.DictReader
            decoded = serialized_bytes.decode("utf-8")
            reader = csv.DictReader(io.StringIO(decoded))
            # Return a list of dictionaries
            return [row for row in reader]
    except (json.JSONDecodeError, UnicodeDecodeError, csv.Error) as exc:
        raise ValueError(f"Failed to deserialize data with method '{serialization_method}': {exc}") from exc