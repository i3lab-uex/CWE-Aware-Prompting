import json
import csv
from io import StringIO

# Safe serialization methods that are allowed for deserialization.
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str):
    """
    Deserialize a byte stream into its corresponding Python object using
    only approved deserialization methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized byte stream to be deserialized.
    deserialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    object
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the requested method is not in SAFE_METHODS or if the data cannot be parsed.
    """
    # Normalise method name
    method = deserialization_method.strip().lower()

    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed or recognized.")

    # Decode bytes to string (UTF‑8) for text based formats
    try:
        text = data_stream.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data stream could not be decoded using UTF‑8.") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON data.") from exc

    if method == "csv":
        try:
            reader = csv.DictReader(StringIO(text))
            # Convert to a list of dictionaries for consistency
            return [row for row in reader]
        except csv.Error as exc:
            raise ValueError("Failed to parse CSV data.") from exc

    # This point should never be reached due to the method check above
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")