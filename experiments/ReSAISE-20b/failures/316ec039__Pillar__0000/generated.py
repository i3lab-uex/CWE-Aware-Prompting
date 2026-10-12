import json
import csv
from io import StringIO, BytesIO
from typing import Any

# Whitelist of safe serialization formats
SAFE_FORMATS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize `serialized_data` using the specified `deserialization_method`.

    Only formats listed in SAFE_FORMATS are allowed. Unsupported or potentially
    dangerous methods raise ValueError.

    Parameters:
        serialized_data (bytes): The byte stream to be deserialized.
        deserialization_method (str): Format name ('json', 'csv').

    Returns:
        Any: The deserialized Python object.

    Raises:
        ValueError: If the method is unsupported or unsafe.
    """
    if deserialization_method not in SAFE_FORMATS:
        raise ValueError(
            f"Unsupported or unsafe deserialization method: {deserialization_method}"
        )

    # Decode bytes to text; assume UTF-8 encoding
    try:
        text = serialized_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data is not valid UTF-8") from exc

    if deserialization_method == "json":
        # json.loads is safe for basic data structures
        return json.loads(text)

    if deserialization_method == "csv":
        # Parse CSV into a list of dictionaries
        f = StringIO(text)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # This point should never be reached due to the whitelist check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")