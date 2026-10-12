import json
import csv
from io import BytesIO, TextIOWrapper

# Registry of allowed serialization methods
ALLOWED_METHODS = {
    "json": json.loads,
    # csv will be handled specially below
}

def restore_object(serialized_bytes: bytes, serialization_method: str):
    """
    Deserialize a Python object from serialized data.

    Parameters
    ----------
    serialized_bytes : bytes
        The byte stream containing the serialized object.
    serialization_method : str
        Identifier of the serialization format. Only 'json' and 'csv'
        are supported for security reasons.

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the method is unrecognized or insecure.
    """
    if serialization_method not in {"json", "csv"}:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    if serialization_method == "json":
        # JSON is safe for deserialization
        return json.loads(serialized_bytes.decode("utf-8"))

    # Handle CSV: read into a list of dictionaries
    if serialization_method == "csv":
        text_stream = TextIOWrapper(BytesIO(serialized_bytes), encoding="utf-8")
        reader = csv.DictReader(text_stream)
        return [row for row in reader]

# Example usage (uncomment to test):
# data = json.dumps({"key": "value"}).encode()
# print(restore_object(data, "json"))
#
# csv_data = b"name,age\nAlice,30\nBob,25"
# print(restore_object(csv_data, "csv"))