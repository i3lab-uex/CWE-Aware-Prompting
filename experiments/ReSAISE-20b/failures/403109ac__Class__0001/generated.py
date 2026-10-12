import json
import csv
from io import StringIO
from typing import Any, List, Dict


# Whitelisted serialization formats
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream according to the specified serialization format.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON, this can be any JSON-compatible type.
        For CSV, a list of dictionaries is returned where each dict represents a row.

    Raises
    ------
    ValueError
        If the method_type is not in the whitelist or if deserialization fails.
    """
    method = method_type.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type}")

    try:
        if method == "json":
            # Ensure the bytes are decoded as UTF-8 before parsing
            text = stream_bytes.decode("utf-8")
            return json.loads(text)

        if method == "csv":
            # Decode bytes to text and use csv.DictReader
            text = stream_bytes.decode("utf-8")
            reader = csv.DictReader(StringIO(text))
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception to provide a consistent error type
        raise ValueError(f"Failed to deserialize stream: {exc}") from exc

    # This point should never be reached due to the whitelist
    raise ValueError(f"Unhandled serialization method: {method_type}")