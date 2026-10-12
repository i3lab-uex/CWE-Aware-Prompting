import json
import csv
import io
from typing import Any

# Predefined list of safe serialization methods
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data.
    format_method : str
        Identifier of the serialization method used ('json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_method is not recognized or disallowed.
    """
    method = format_method.lower()
    if method not in SAFE_METHODS:
        raise ValueError(f"Unsupported or disallowed serialization format: {format_method}")

    # Decode bytes to text for processing
    try:
        text = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF‑8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # Use csv.DictReader to produce a list of dictionaries
        try:
            f = io.StringIO(text)
            reader = csv.DictReader(f)
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc