import json
import csv
import io

# Define the set of allowed serialization methods.
SAFE_SERIALIZERS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str):
    """
    Deserialize a byte stream into its corresponding Python object using a
    safe, whitelisted serialization method.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data as a byte stream.
    method_of_serialization : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is not recognized or is disallowed.
    """
    if method_of_serialization not in SAFE_SERIALIZERS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed.")

    if method_of_serialization == "json":
        # JSON deserialization using json.loads on a UTF-8 decoded string.
        try:
            text = data_bytes_stream.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to deserialize JSON data.") from exc

    if method_of_serialization == "csv":
        # CSV deserialization: parse into a list of dictionaries.
        try:
            text_stream = io.StringIO(data_bytes_stream.decode("utf-8"))
            reader = csv.DictReader(text_stream)
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError("Failed to decode CSV data.") from exc

    # This point should never be reached because of the whitelist check.
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")