import json
import csv
import io
from typing import Any, List, Dict

# Define the list of safe deserialization methods
SAFE_METHODS = {"json", "csv"}

def deserialize_data(data_stream: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only safe methods.

    Parameters
    ----------
    data_stream : bytes
        The serialized byte stream.
    deserialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it returns a native Python
        data structure (dict, list, etc.). For CSV it returns a list of
        dictionaries mapping column names to values.

    Raises
    ------
    ValueError
        If the method is not recognized or not in the safe list.
    """
    method = deserialization_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{deserialization_method}' is not allowed.")

    # Convert bytes to a text stream using UTF-8 (common encoding for JSON/CVS)
    try:
        text_stream = io.TextIOWrapper(io.BytesIO(data_stream), encoding="utf-8")
    except Exception as exc:
        raise ValueError("Failed to interpret data stream as UTF-8 text.") from exc

    if method == "json":
        # JSON deserialization is safe as it only constructs basic data types
        try:
            return json.load(text_stream)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data.") from exc

    if method == "csv":
        # CSV deserialization into a list of dicts (header-based)
        try:
            reader = csv.DictReader(text_stream)
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data.") from exc

    # Should never reach here due to the SAFE_METHODS check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")