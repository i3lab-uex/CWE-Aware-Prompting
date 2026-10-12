import json
import csv
import io
from typing import Any, List, Dict

# Define the set of trusted serialization formats.
TRUSTED_FORMATS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a Python object from serialized byte data using only
    trusted serialization formats.

    Parameters:
        serialized_data (bytes): The raw byte stream to be deserialized.
        deserialization_method (str): The name of the serialization format
            ('json', 'csv', etc.).

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the requested format is not trusted or unsupported.
    """
    method = deserialization_method.lower()

    if method not in TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe deserialization method: '{deserialization_method}'. "
            f"Allowed methods are: {', '.join(TRUSTED_FORMATS)}."
        )

    if method == "json":
        # JSON is safe for basic data types; decode bytes to string first.
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF-8 data for JSON deserialization") from exc
        return json.loads(text)

    if method == "csv":
        # CSV deserialization returns a list of dictionaries.
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Invalid UTF-8 data for CSV deserialization") from exc

        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check.
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")