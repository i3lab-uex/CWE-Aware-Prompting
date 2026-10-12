import json
import csv
from io import BytesIO, StringIO

# Define the set of serialization methods that are considered safe.
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str):
    """
    Deserialize a byte stream into its corresponding Python object using only
    safe, predefined deserialization methods.

    Parameters:
        data_stream (bytes): The serialized data.
        deserialization_method (str): Identifier of the serialization method
                                      used ('json', 'csv').

    Returns:
        The deserialized Python object (e.g., dict, list, or list of lists).

    Raises:
        ValueError: If the method is not recognized or disallowed.
        json.JSONDecodeError: If JSON decoding fails.
        csv.Error: If CSV parsing fails.
    """
    method = deserialization_method.lower()

    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Common helper: convert bytes to text
    try:
        text = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream is not valid UTF-8.") from exc

    if method == "json":
        # json.loads safely parses JSON into Python objects
        return json.loads(text)

    if method == "csv":
        # Parse CSV into a list of rows, each row is a list of strings
        csv_file = StringIO(text)
        reader = csv.reader(csv_file)
        return [row for row in reader]

    # The above guard should make this unreachable, but keep it as a safety net.
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")