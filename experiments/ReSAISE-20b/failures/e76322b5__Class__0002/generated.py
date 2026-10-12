import json
import csv
from io import TextIOWrapper, StringIO
from typing import Any

# Define the set of safe serialization formats that are permitted.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize the given byte stream according to the specified format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        Name of the serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For CSV data this will be a list of
        dictionaries, each representing a row.

    Raises
    ------
    ValueError
        If the format_name is not in ALLOWED_FORMATS or if deserialization fails.
    """
    # Normalise the format name to lower case for comparison
    fmt = format_name.lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name}")

    try:
        if fmt == "json":
            # JSON expects text, so decode using UTF-8
            return json.loads(encoded_bytes.decode("utf-8"))
        elif fmt == "csv":
            # CSV is text based; decode and use DictReader
            csv_text = encoded_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(csv_text))
            return [row for row in reader]
    except Exception as exc:
        # Wrap any exception from the deserialization libraries into a ValueError
        raise ValueError(f"Failed to deserialize data: {exc}") from exc

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_name}")