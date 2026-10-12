import json
import csv
import io
from typing import Any, List, Dict

# Allowed serialization methods – only safe formats are registered.
ALLOWED_METHODS = {
    "json": "JSON",
    "csv": "CSV",
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from an untrusted byte stream.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw data to deserialize.
    serialization_method : str
        Identifier of the serialization format.  Only formats listed in
        ``ALLOWED_METHODS`` are accepted.

    Returns
    -------
    Any
        The deserialized Python object.  For JSON this is typically a dict or
        list; for CSV it is a list of dictionaries.

    Raises
    ------
    ValueError
        If the supplied method is not in ``ALLOWED_METHODS`` or if the data
        cannot be parsed.
    """
    method = serialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {serialization_method}")

    try:
        if method == "json":
            # json.loads expects a str, so decode using UTF-8.
            return json.loads(serialized_bytes.decode("utf-8"))
        elif method == "csv":
            # CSV is interpreted as a list of dictionaries.
            text_stream = io.StringIO(serialized_bytes.decode("utf-8"))
            reader = csv.DictReader(text_stream)
            return [row for row in reader]
    except Exception as exc:
        # Wrap any parsing error into a ValueError to avoid leaking internal
        # exception details.
        raise ValueError(f"Failed to deserialize data with method '{serialization_method}': {exc}") from exc