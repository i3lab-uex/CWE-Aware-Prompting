import json
import csv
from io import StringIO
from typing import Any

# A set of serialization methods that are considered safe for deserialization.
SAFE_SERIALIZERS = {
    "json",
    "csv",
}

def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Reconstruct a Python object from a serialized byte stream.

    Parameters
    ----------
    deserialized_bytes : bytes
        The raw byte stream containing the serialized data.
    method_for_serialization : str
        A string identifying the serialization format used. Supported values are:
            - "json": JSON encoded data.
            - "csv" : CSV formatted data. The function returns a list of dictionaries,
                      one per row.

    Returns
    -------
    Any
        The Python object represented by the serialized data.

    Raises
    ------
    ValueError
        If `method_for_serialization` is not in the list of supported formats,
        or if the data cannot be decoded/parsed using the specified method.
    """
    # Normalize and validate the requested serialization method
    method = method_for_serialization.lower()
    if method not in SAFE_SERIALIZERS:
        raise ValueError(f"Unsupported or unsafe serialization format: '{method_for_serialization}'")

    # Convert bytes to text for parsing
    try:
        text = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded using UTF-8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Failed to parse JSON data") from exc

    if method == "csv":
        # Using csv.DictReader to interpret each row as a dictionary
        try:
            f = StringIO(text)
            reader = csv.DictReader(f)
            return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {method_for_serialization}")