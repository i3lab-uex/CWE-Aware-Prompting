import json
import csv
import io
from typing import Any, List, Dict

# Define the list of safe serialization methods.
SAFE_METHODS = {"json", "csv"}


def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    authorized methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized data as a byte string.
    deserialization_method : str
        Identifier of the serialization format ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it returns the parsed data.
        For CSV it returns a list of dictionaries (one per row).

    Raises
    ------
    ValueError
        If the requested deserialization method is not in SAFE_METHODS.
    """
    if deserialization_method.lower() not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Decode bytes to a string using UTF-8. This is safe for JSON and CSV.
    text = data_stream.decode("utf-8")

    if deserialization_method.lower() == "json":
        return json.loads(text)

    # CSV handling
    if deserialization_method.lower() == "csv":
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]


# Example usage (commented out):
# if __name__ == "__main__":
#     json_bytes = b'{"name": "Alice", "age": 30}'
#     print(deserialize_data(json_bytes, "json"))
#
#     csv_bytes = b'name,age\nAlice,30\nBob,25'
#     print(deserialize_data(csv_bytes, "csv"))