import json
import csv
from io import TextIOWrapper, BytesIO
from typing import Any

# Define the set of serialization methods that are considered safe.
SAFE_METHODS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize `serialized_data` using the specified method.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream to be deserialized.
    deserialization_method : str
        The serialization format: 'json' or 'csv'.

    Returns
    -------
    Any
        The Python object produced by deserialization.

    Raises
    ------
    ValueError
        If the method is not in SAFE_METHODS or if the data cannot be parsed.
    """
    # Normalise method name to lower case
    method = deserialization_method.lower()

    if method not in SAFE_METHODS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {deserialization_method!r}")

    # JSON handling
    if method == "json":
        try:
            text = serialized_data.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Failed to decode JSON data") from exc

    # CSV handling
    if method == "csv":
        try:
            with BytesIO(serialized_data) as bio:
                # Use TextIOWrapper to convert bytes to text
                with TextIOWrapper(bio, encoding="utf-8") as txt:
                    reader = csv.DictReader(txt)
                    # Return list of dictionaries
                    return [row for row in reader]
        except Exception as exc:
            raise ValueError("Failed to parse CSV data") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled deserialization method: {deserialization_method!r}")