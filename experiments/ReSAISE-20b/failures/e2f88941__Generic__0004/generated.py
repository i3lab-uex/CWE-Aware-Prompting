import json
import csv
import io
from typing import Any, List

# Define the set of allowed serialization methods.
ALLOWED_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data in bytes.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it will be a dict or list.
        For CSV it will be a list of rows, where each row is a list of strings.

    Raises
    ------
    ValueError
        If the serialization method is not in ALLOWED_METHODS.
    """
    if format_method not in ALLOWED_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or recognized.")

    # Decode bytes to text using UTF-8. This is safe for JSON and CSV.
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data bytes could not be decoded using UTF-8.") from exc

    if format_method == "json":
        # json.loads can raise JSONDecodeError; let it propagate as ValueError for consistency.
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to decode JSON data.") from exc

    if format_method == "csv":
        # Use csv.reader to parse CSV data. Return a list of rows.
        reader = csv.reader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the ALLOWED_METHODS check.
    raise ValueError(f"Unhandled serialization method: {format_method}")