import json
import csv
from io import BytesIO

# Define the set of serialization methods that are considered safe.
SAFE_METHODS = {"json", "csv"}

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into its corresponding Python object using only
    approved serialization methods.

    Parameters
    ----------
    data_bytes : bytes
        The byte stream that contains the serialized data.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    object
        The deserialized Python object (e.g., dict, list).

    Raises
    ------
    ValueError
        If the provided serialization method is not in SAFE_METHODS.
    """
    if format_method not in SAFE_METHODS:
        raise ValueError(f"Unsupported or unsafe serialization method: {format_method}")

    # ------------------------------------------------------------------
    # JSON deserialization
    # ------------------------------------------------------------------
    if format_method == "json":
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    # ------------------------------------------------------------------
    # CSV deserialization
    # ------------------------------------------------------------------
    if format_method == "csv":
        try:
            text = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("CSV data is not valid UTF-8") from exc
        # Use BytesIO to mimic a file object for csv.DictReader
        buffer = BytesIO(text.encode("utf-8"))
        reader = csv.DictReader(TextIOWrapper(buffer, encoding="utf-8"))
        return [row for row in reader]