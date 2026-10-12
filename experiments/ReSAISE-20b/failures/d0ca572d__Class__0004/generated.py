import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# List of allowed serialization methods (whitelist)
SAFE_SERIALIZATION_METHODS = {"json", "csv"}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    approved serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized data in binary form.
    method_of_serialization : str
        Identifier of the serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object (e.g., dict, list, etc.).

    Raises
    ------
    ValueError
        If the provided method is not in the whitelist or if deserialization fails.
    """
    # Normalise method name
    method = method_of_serialization.strip().lower()

    if method not in SAFE_SERIALIZATION_METHODS:
        raise ValueError(f"Deserialization method '{method_of_serialization}' is not allowed or recognized.")

    try:
        if method == "json":
            # json expects text, so decode bytes to str using UTF-8
            return json.loads(data_bytes_stream.decode("utf-8"))

        elif method == "csv":
            # csv works on text streams; wrap bytes with a TextIOWrapper
            stream = TextIOWrapper(BytesIO(data_bytes_stream), encoding="utf-8")
            reader = csv.DictReader(stream)
            # Return list of dictionaries
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception into ValueError to keep the API consistent
        raise ValueError(f"Failed to deserialize data using method '{method_of_serialization}': {exc}") from exc