import json
import csv
from io import StringIO, BytesIO

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str):
    """
    Deserialize a byte stream into its corresponding Python object using only
    authorized methods.

    Parameters:
        data_stream (bytes): The serialized data.
        deserialization_method (str): Identifier of the serialization method
            ('json' or 'csv').

    Returns:
        The deserialized Python object.

    Raises:
        ValueError: If the method is disallowed or not recognized.
    """
    if deserialization_method.lower() not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    if deserialization_method.lower() == "json":
        # Decode bytes to string before JSON parsing
        text = data_stream.decode("utf-8")
        return json.loads(text)

    if deserialization_method.lower() == "csv":
        # Treat the data as a CSV file and return list of dictionaries
        text = data_stream.decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # In case new safe methods are added in future
    raise ValueError(f"Deserialization method '{deserialization_method}' is not implemented.")