import json
import csv
from io import StringIO, BytesIO
from typing import Any

# Define the list of safe deserialization methods.
SAFE_METHODS = {"json", "csv"}


def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    approved, safe methods.

    Parameters:
        data_stream (bytes): The serialized data as bytes.
        deserialization_method (str): Identifier of the serialization method
            used ('json', 'csv').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the method is not recognized or disallowed.
    """
    if deserialization_method not in SAFE_METHODS:
        raise ValueError(
            f"Deserialization method '{deserialization_method}' is not allowed."
        )

    # Common decoding step: assume UTF-8 encoding for text-based formats.
    try:
        decoded = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream is not valid UTF-8 encoded text.") from exc

    if deserialization_method == "json":
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if deserialization_method == "csv":
        # Treat the CSV as a list of dictionaries (first row as headers).
        f = StringIO(decoded)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # This point should never be reached because of the earlier check.
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")