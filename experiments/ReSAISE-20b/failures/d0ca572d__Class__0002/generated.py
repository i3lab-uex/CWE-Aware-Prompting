import json
import csv
from io import BytesIO, TextIOWrapper

# Define the set of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into a Python object using only
    approved serialization methods.

    Parameters:
        data_bytes_stream (bytes): The serialized data.
        method_of_serialization (str): Identifier of the serialization
            format used ('json', 'csv').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the method is not recognized or disallowed.
    """
    if method_of_serialization.lower() not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or disallowed serialization method: "
                         f"{method_of_serialization}")

    # JSON deserialization
    if method_of_serialization.lower() == "json":
        try:
            # Decode bytes to string safely
            text = data_bytes_stream.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data") from exc

    # CSV deserialization
    if method_of_serialization.lower() == "csv":
        try:
            # Wrap bytes in a text IO wrapper for csv module
            buffer = BytesIO(data_bytes_stream)
            # Use UTF-8 decoding; ignore errors to avoid crashes on bad data
            text_wrapper = TextIOWrapper(buffer, encoding="utf-8", errors="replace")
            reader = csv.DictReader(text_wrapper)
            # Convert to list of dictionaries
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to deserialize CSV data") from exc