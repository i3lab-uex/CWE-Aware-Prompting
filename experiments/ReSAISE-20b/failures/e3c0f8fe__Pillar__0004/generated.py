import json
import csv
import io
from typing import Any

# Registry of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}


def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from a byte stream.

    Parameters
    ----------
    serialized_bytes : bytes
        The raw data to deserialize.
    serialization_method : str
        Identifier of the serialization format. Must be one of ALLOWED_METHODS.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the serialization method is unrecognized or considered insecure.
    """
    if not isinstance(serialized_bytes, (bytes, bytearray)):
        raise TypeError("serialized_bytes must be bytes-like")

    method = serialization_method.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {serialization_method}")

    # Decode bytes to text for JSON and CSV
    try:
        text = serialized_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Unable to decode bytes as UTF-8") from exc

    if method == "json":
        # json.loads is safe for basic data structures
        return json.loads(text)

    if method == "csv":
        # Return a list of dictionaries, one per row
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # The following line is unreachable due to the earlier check,
    # but it satisfies type-checkers.
    raise ValueError(f"Unhandled serialization method: {serialization_method}")