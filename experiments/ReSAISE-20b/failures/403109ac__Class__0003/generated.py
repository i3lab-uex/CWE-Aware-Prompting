import json
import csv
from io import BytesIO, StringIO
from typing import Any, List, Dict


# Define the set of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format used. Must be one of the values in ALLOWED_METHODS.

    Returns
    -------
    Any
        The deserialized Python object. For 'json' this is whatever json.loads returns.
        For 'csv' this is a list of dictionaries, one per row.

    Raises
    ------
    ValueError
        If the method_type is not supported or potentially insecure.
    """
    # Normalise and validate the method type
    method = method_type.strip().lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(
            f"Unsupported or insecure serialization method: '{method_type}'. "
            f"Allowed methods are: {', '.join(sorted(ALLOWED_METHODS))}."
        )

    # Perform the appropriate deserialization
    if method == "json":
        try:
            return json.loads(stream_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        try:
            # CSV is text-based; decode to str first
            text = stream_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("CSV data must be UTF‑8 encoded") from exc

        # Use StringIO to provide a file-like object for csv.DictReader
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # The code should never reach here due to the earlier validation
    raise ValueError(f"Unhandled serialization method: {method}")