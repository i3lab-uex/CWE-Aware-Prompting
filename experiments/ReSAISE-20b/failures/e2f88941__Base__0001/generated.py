import json
import csv
import io
from typing import Any

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using a safe, whitelisted method.

    Parameters
    ----------
    data_bytes : bytes
        The byte stream containing the serialized data.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_method is not in ALLOWED_FORMATS or if deserialization fails.
    """
    method = format_method.lower()
    if method not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or disallowed serialization format: {format_method}")

    try:
        if method == "json":
            # json.loads expects a string, so decode bytes using UTF-8.
            return json.loads(data_bytes.decode("utf-8"))
        elif method == "csv":
            # CSV is treated as a sequence of rows; we return a list of dicts.
            text = data_bytes.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]
    except Exception as exc:
        # Wrap any exception into ValueError to avoid leaking internal details.
        raise ValueError(f"Deserialization error for format '{format_method}': {exc}") from exc