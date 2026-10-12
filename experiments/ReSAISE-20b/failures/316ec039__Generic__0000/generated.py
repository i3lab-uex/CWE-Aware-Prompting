import json
import csv
import io
from typing import Any, List, Dict

# A set of serialization formats that are considered safe for deserialization.
TRUSTED_FORMATS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a byte stream into a Python object using only trusted formats.

    Parameters
    ----------
    serialized_data : bytes
        The data stream to be deserialized.
    deserialization_method : str
        The serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object recovered from the serialized byte stream.

    Raises
    ------
    ValueError
        If an unsupported or potentially harmful serialization method is requested.
    """
    method = deserialization_method.lower()

    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method}")

    if method == "json":
        # JSON is safe as long as the input is properly formatted.
        try:
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # For CSV, return a list of dictionaries (one per row).
        try:
            text = serialized_data.decode("utf-8")
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid CSV data") from exc

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")