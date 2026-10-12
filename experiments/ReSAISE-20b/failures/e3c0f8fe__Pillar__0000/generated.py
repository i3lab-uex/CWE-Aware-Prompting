import json
import csv
import io
from typing import Any

# Registry of allowed serialization methods.
ALLOWED_METHODS = {
    "json",
    "csv",   # CSV is treated as a list of dictionaries.
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Restore a Python object from a serialized data stream.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw byte stream containing the serialized data.
    serialization_method : str
        Identifier of the serialization format. Supported values are:
            - 'json'
            - 'csv'

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in the allowed registry or if deserialization fails.
    """
    # Ensure the method is explicitly permitted.
    if serialization_method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {serialization_method}")

    try:
        if serialization_method == "json":
            # Decode bytes to string using UTF-8 (JSON is text-based).
            json_str = serialized_bytes.decode("utf-8")
            return json.loads(json_str)

        elif serialization_method == "csv":
            # CSV is decoded as UTF-8 and parsed into a list of dictionaries.
            csv_str = serialized_bytes.decode("utf-8")
            reader = csv.DictReader(io.StringIO(csv_str))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception in a ValueError to keep the API consistent.
        raise ValueError(f"Failed to deserialize using {serialization_method}: {exc}") from exc