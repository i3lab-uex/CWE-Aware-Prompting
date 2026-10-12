import json
import csv
import io
from typing import Any, List, Dict

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    authorized, safe deserialization methods.

    Parameters:
        data_stream (bytes): The serialized data as a byte stream.
        deserialization_method (str): Identifier of the serialization method
            used (e.g., 'json', 'csv').

    Returns:
        Any: The deserialized Python object. For JSON, this may be a dict,
             list, str, etc. For CSV, a list of dictionaries (one per row).

    Raises:
        ValueError: If the deserialization method is not recognized or
                    disallowed.
    """
    method = deserialization_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed or recognized.")

    # Decode bytes to text safely (UTF-8) – any decoding errors raise an exception
    try:
        text_data = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream could not be decoded using UTF-8.") from exc

    if method == "json":
        try:
            return json.loads(text_data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if method == "csv":
        # Use StringIO to allow csv module to read the text
        try:
            reader = csv.DictReader(io.StringIO(text_data))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data.") from exc

    # This point should never be reached due to the SAFE_METHODS check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")