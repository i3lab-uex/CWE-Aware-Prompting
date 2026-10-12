import json
import csv
import io
from typing import Any, List, Dict

# Registry of allowed serialization methods
ALLOWED_METHODS = {
    "json": "JSON",
    "csv": "CSV",
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize `serialized_bytes` using the specified `serialization_method`.

    Only trusted formats listed in ALLOWED_METHODS are permitted.
    Unsupported or insecure methods raise ValueError.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unknown or insecure.
    """
    # Normalise method name to lowercase for comparison
    method = serialization_method.strip().lower()

    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    # Ensure the input is bytes; decode to text for JSON and CSV
    try:
        text = serialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8 encoded text") from exc

    if method == "json":
        # json.loads safely parses JSON into native Python types
        return json.loads(text)

    if method == "csv":
        # Use csv.DictReader to parse CSV into a list of dictionaries
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {serialization_method}")