import json
import csv
from io import StringIO

# List of serialization methods that are considered safe for deserialization.
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The byte stream that contains the serialized data.
    format_method : str
        Identifier for the serialization method used ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the specified format_method is not in SAFE_METHODS or if decoding fails.
    """
    # Ensure the method is known and safe
    method = format_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed.")

    # Convert bytes to a text string. Assume UTF‑8 encoding; raise if invalid.
    try:
        data_str = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Byte data could not be decoded using UTF‑8.") from exc

    if method == "json":
        # json.loads is safe for the intended data structures (dict, list, str, int, float, bool, None)
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if method == "csv":
        # Use csv.DictReader to parse CSV into a list of dictionaries.
        # Only the standard library's CSV reader is used, which does not evaluate arbitrary code.
        try:
            with StringIO(data_str) as csv_file:
                reader = csv.DictReader(csv_file)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data.") from exc