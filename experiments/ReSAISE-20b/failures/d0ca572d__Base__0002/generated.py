import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any

# List of methods that are considered safe for deserialization.
SAFE_SERIALIZERS = {
    "json",
    "csv",   # CSV is treated as a list of dictionaries.
}

def rebuild_object(data_bytes_stream: bytes, method_of_serialization: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using
    only approved serialization methods.

    Parameters
    ----------
    data_bytes_stream : bytes
        The serialized byte stream to be deserialized.
    method_of_serialization : str
        Identifier of the serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested method is not in SAFE_SERIALIZERS or is unsupported.
    """
    if method_of_serialization not in SAFE_SERIALIZERS:
        raise ValueError(
            f"Deserialization method '{method_of_serialization}' is not allowed."
        )

    # Ensure the data stream is decoded correctly for text-based formats.
    if method_of_serialization == "json":
        try:
            decoded = data_bytes_stream.decode("utf-8")
            return json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method_of_serialization == "csv":
        # Treat CSV as a list of dictionaries (first row is header).
        try:
            with TextIOWrapper(BytesIO(data_bytes_stream), encoding="utf-8") as text_io:
                reader = csv.DictReader(text_io)
                return [row for row in reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc

    # In practice, this point is unreachable because of the earlier check,
    # but we keep it for completeness.
    raise ValueError(f"Unhandled serialization method: {method_of_serialization}")