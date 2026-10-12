import json
import csv
from io import BytesIO

# Predefined set of accepted serialization formats
ALLOWED_FORMATS = {"json", "csv"}

def deserialize_object(raw_data: bytes, format_type: str):
    """
    Deserialize a byte stream into a Python object.

    Parameters
    ----------
    raw_data : bytes
        The serialized input stream.
    format_type : str
        The serialization format used ('json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not supported or insecure.
    """
    if not isinstance(raw_data, bytes):
        raise ValueError("raw_data must be of type 'bytes'")

    fmt = format_type.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_type}")

    if fmt == "json":
        # Decode bytes to string, then parse JSON
        try:
            text = raw_data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("JSON data is not valid UTF-8") from exc
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if fmt == "csv":
        # Treat the bytes as a CSV file and return a list of dicts
        try:
            stream = BytesIO(raw_data)
            reader = csv.DictReader(
                (line.decode("utf-8") for line in stream),
                skipinitialspace=True,
            )
        except Exception as exc:
            raise ValueError("Failed to read CSV data") from exc
        return list(reader)

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled format: {format_type}")