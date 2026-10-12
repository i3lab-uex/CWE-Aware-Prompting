import io
import csv
import json
from typing import Any, Dict

# Registry of allowed serialization methods
ALLOWED_METHODS: Dict[str, str] = {
    "json": "JSON",
    "csv": "CSV",
}

def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from a byte stream.

    Parameters
    ----------
    serialized_bytes : bytes
        The data to deserialize.
    serialization_method : str
        Identifier of the serialization format. Only keys in ALLOWED_METHODS are accepted.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is not recognized or considered insecure.
    """
    # Normalise the method name
    method = serialization_method.strip().lower()

    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: '{serialization_method}'")

    # JSON deserialization
    if method == "json":
        try:
            return json.loads(serialized_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON") from exc

    # CSV deserialization
    if method == "csv":
        try:
            with io.BytesIO(serialized_bytes) as buffer:
                text_stream = io.TextIOWrapper(buffer, encoding="utf-8", newline="")
                reader = csv.DictReader(text_stream)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV") from exc

    # This point should never be reached because of the registry check
    raise ValueError(f"Unhandled serialization method: '{serialization_method}'")