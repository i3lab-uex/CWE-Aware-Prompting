import json
import csv
import io
from typing import Any

# List of serialization formats that are considered safe for deserialization.
TRUSTED_FORMATS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Safely deserialize `serialized_data` according to the specified
    `deserialization_method`.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized data.
    deserialization_method : str
        One of the trusted serialization formats: 'json' or 'csv'.

    Returns
    -------
    Any
        The Python object resulting from deserialization.

    Raises
    ------
    ValueError
        If the serialization method is not in TRUSTED_FORMATS or if
        deserialization fails due to malformed data.
    """
    method = deserialization_method.lower()

    if method not in TRUSTED_FORMATS:
        raise ValueError(
            f"Unsupported or potentially harmful deserialization method: {deserialization_method}"
        )

    # Decode bytes to text using UTF-8. Errors are replaced to avoid crashes.
    try:
        text = serialized_data.decode("utf-8", errors="replace")
    except Exception as exc:
        raise ValueError(f"Failed to decode data: {exc}") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if method == "csv":
        try:
            # Use StringIO to allow csv module to read from the string.
            reader = csv.DictReader(io.StringIO(text))
            return [row for row in reader]
        except Exception as exc:
            raise ValueError(f"Failed to parse CSV data: {exc}") from exc

    # Should never reach here because of the TRUSTED_FORMATS check.
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")