import json
import csv
import io
from typing import Any, List, Dict


# Allowed serialization formats (safe and supported)
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
        The deserialized Python object.  For CSV, a list of dictionaries is returned.
        For JSON, the result of json.loads() is returned.

    Raises
    ------
    ValueError
        If an unsupported or insecure serialization method is requested.
    """
    # Normalise the method name to avoid accidental case‑sensitive mismatches
    method = method_type.strip().lower()

    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: '{method_type}'")

    # Decode bytes to text (UTF‑8 is the de facto standard for JSON/CVS)
    try:
        decoded = stream_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input stream is not valid UTF‑8 encoded text") from exc

    # Use a context manager to ensure that any temporary resources are released
    if method == "json":
        try:
            return json.loads(decoded)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    elif method == "csv":
        # csv.DictReader requires a file‑like object; io.StringIO provides that
        with io.StringIO(decoded) as csv_file:
            reader = csv.DictReader(csv_file)
            # Convert the iterator to a list of dictionaries
            return [row for row in reader]

    # The code path should never reach here because of the earlier check
    raise ValueError(f"Unhandled serialization method: '{method_type}'")