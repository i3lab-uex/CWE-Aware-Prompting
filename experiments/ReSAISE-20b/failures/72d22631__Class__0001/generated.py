import json
import csv
from io import StringIO
from typing import Any


def recover_obj(deserialized_bytes: bytes, method_for_serialization: str) -> Any:
    """
    Safely reconstruct a Python object from a byte stream using only trusted
    serialization methods.

    Parameters
    ----------
    deserialized_bytes : bytes
        The raw byte stream to be deserialized.
    method_for_serialization : str
        The name of the serialization format. Supported values are:
            - 'json'
            - 'csv'

    Returns
    -------
    Any
        The Python object produced by deserializing the input bytes.

    Raises
    ------
    ValueError
        If an unsupported or potentially dangerous serialization method is requested.
    """
    # Define the set of trusted, safe serialization formats
    TRUSTED_METHODS = {"json", "csv"}

    # Normalise the method name to lower case
    method = method_for_serialization.strip().lower()

    if method not in TRUSTED_METHODS:
        raise ValueError(
            f"Unsupported or unsafe serialization method: {method_for_serialization!r}"
        )

    # Decode the bytes to a string using UTF‑8 (most common encoding for text formats)
    try:
        decoded = deserialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes are not valid UTF‑8") from exc

    if method == "json":
        # Use json.loads which is safe for JSON data
        return json.loads(decoded)

    if method == "csv":
        # Parse CSV into a list of dictionaries
        csv_reader = csv.DictReader(StringIO(decoded))
        return [row for row in csv_reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {method}")