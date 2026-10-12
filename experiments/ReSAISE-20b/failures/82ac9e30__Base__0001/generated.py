import json
import csv
import io
from typing import Any, List, Dict

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    authorized deserialization techniques.

    Parameters:
        data_stream (bytes): The serialized data.
        deserialization_method (str): Identifier of the serialization method
                                      used ('json', 'csv').

    Returns:
        The deserialized Python object. For JSON it returns the parsed
        structure (dict/list/etc.). For CSV it returns a list of rows,
        each row being either a list (default) or a dict if header is present.

    Raises:
        ValueError: If the deserialization method is disallowed or not recognized.
    """
    method = deserialization_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Convert bytes to string safely
    try:
        text = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream is not valid UTF-8 encoded text.") from exc

    if method == "json":
        # json.loads is safe for basic data types (dict, list, str, int, float, bool, None)
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if method == "csv":
        # Use csv module with default settings; returns list of lists
        try:
            reader = csv.reader(io.StringIO(text))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data.") from exc

    # This point should never be reached due to the SAFE_METHODS check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")