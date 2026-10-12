import json
import csv
import io
from typing import Any

# Registry of allowed serialization methods
ALLOWED_METHODS = {"json", "csv"}


def restore_object(serialized_bytes: bytes, serialization_method: str) -> Any:
    """
    Deserialize a Python object from the given byte stream.

    Parameters
    ----------
    serialized_bytes : bytes
        The data stream to deserialize.
    serialization_method : str
        Identifier of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The Python object obtained from deserialization.

    Raises
    ------
    ValueError
        If the method is unrecognized or considered insecure.
    """
    if serialization_method not in ALLOWED_METHODS:
        raise ValueError(f"Unrecognized or insecure serialization method: {serialization_method}")

    if serialization_method == "json":
        # Decode bytes to str and parse JSON
        try:
            text = serialized_bytes.decode("utf-8")
            return json.loads(text)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid JSON data: {exc}") from exc

    if serialization_method == "csv":
        # Interpret bytes as UTF‑8 encoded CSV
        try:
            text_io = io.StringIO(serialized_bytes.decode("utf-8"))
            reader = csv.DictReader(text_io)
            return [row for row in reader]
        except UnicodeDecodeError as exc:
            raise ValueError(f"Invalid CSV encoding: {exc}") from exc

    # In practice this point is unreachable because of the ALLOWED_METHODS check,
    # but keeping it for completeness.
    raise ValueError(f"Unsupported serialization method: {serialization_method}")