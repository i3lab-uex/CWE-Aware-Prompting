import json
import csv
from io import BytesIO
from typing import Any

# Registry of safe serialization methods
ALLOWED_METHODS = {"json", "csv"}


def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from serialized_bytes using the specified method.

    Parameters
    ----------
    serialized_bytes : bytes
        The byte stream containing the serialized data.
    serialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unrecognized or considered insecure.
    """
    method = serialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    # Use a BytesIO wrapper to provide a file-like object for csv and json
    with BytesIO(serialized_bytes) as buffer:
        if method == "json":
            # JSON expects text; decode bytes to str safely
            try:
                text = buffer.read().decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("JSON data is not valid UTF-8") from exc
            try:
                return json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError("Failed to parse JSON") from exc

        if method == "csv":
            # CSV is parsed into a list of dictionaries
            try:
                buffer.seek(0)
                reader = csv.DictReader(
                    (line.decode("utf-8") for line in buffer),  # decode each row
                )
                return [row for row in reader]
            except Exception as exc:
                raise ValueError("Failed to parse CSV") from exc