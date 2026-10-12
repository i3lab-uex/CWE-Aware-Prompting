import json
import csv
import io
from typing import Any

# Registry of allowed serialization methods.
ALLOWED_METHODS = {
    "json": "json",
    "csv": "csv",
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize `serialized_bytes` using the specified method.

    Parameters
    ----------
    serialized_bytes : bytes
        The data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object reconstructed from the serialized data.

    Raises
    ------
    ValueError
        If `serialization_method` is not in the allowed registry or if deserialization fails.
    """
    method = ALLOWED_METHODS.get(serialization_method.lower())
    if not method:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    try:
        if method == "json":
            # Decode bytes to string and parse JSON
            text = serialized_bytes.decode("utf-8")
            return json.loads(text)

        elif method == "csv":
            # Interpret bytes as a CSV file and return list of dicts
            with io.BytesIO(serialized_bytes) as buffer:
                text_stream = io.TextIOWrapper(buffer, encoding="utf-8")
                reader = csv.DictReader(text_stream)
                return [row for row in reader]

    except Exception as exc:
        # Wrap any exception to avoid leaking sensitive information
        raise ValueError(f"Deserialization failed for method '{serialization_method}': {exc}") from exc