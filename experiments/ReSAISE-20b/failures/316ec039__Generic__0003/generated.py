import json
import csv
from io import StringIO, BytesIO
from typing import Any

# Define the set of serialization methods that are considered safe.
SAFE_SERIALIZATION_METHODS = {"json", "csv"}

def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize `serialized_data` using the specified method.

    Parameters
    ----------
    serialized_data : bytes
        The byte stream containing the serialized object.
    deserialization_method : str
        Name of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unsupported or potentially unsafe.
    """
    method = deserialization_method.lower()
    if method not in SAFE_SERIALIZATION_METHODS:
        raise ValueError(
            f"Unsupported or unsafe deserialization method: '{deserialization_method}'. "
            f"Allowed methods are: {', '.join(sorted(SAFE_SERIALIZATION_METHODS))}"
        )

    # Ensure the input is bytes; if it's a string, encode it.
    if not isinstance(serialized_data, (bytes, bytearray)):
        raise TypeError("serialized_data must be bytes or bytearray")

    if method == "json":
        # JSON expects a text stream; decode UTF-8.
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        return json.loads(text)

    if method == "csv":
        # CSV is read as text; decode UTF-8.
        try:
            text = serialized_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("CSV data is not valid UTF-8") from exc

        # Use StringIO to provide a file-like object for csv.DictReader.
        f = StringIO(text)
        reader = csv.DictReader(f)
        # Return a list of dictionaries (one per row).
        return [row for row in reader]

    # The check above guarantees we never reach here, but keep a guard.
    raise ValueError(f"Unhandled deserialization method: {deserialization_method}")