import json
import csv
import io
from typing import Any, List

# Define the set of serialization formats that are considered safe and allowed.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` according to the specified serialization format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        Name of the serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.  For JSON this is a native Python structure.
        For CSV this is a list of rows, where each row is represented as a list of strings.

    Raises
    ------
    ValueError
        If the requested format is not in ALLOWED_FORMATS or if deserialization fails.
    """
    # Normalise the format name to lower case for comparison
    fmt = format_name.lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: '{format_name}'")

    try:
        if fmt == "json":
            # JSON expects a string; decode bytes to UTF-8
            text = encoded_bytes.decode("utf-8")
            return json.loads(text)

        if fmt == "csv":
            # CSV is read as text; each row is a list of strings
            text = encoded_bytes.decode("utf-8")
            reader = csv.reader(io.StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into a ValueError to avoid leaking internal details
        raise ValueError(f"Failed to decode data using format '{format_name}': {exc}") from None