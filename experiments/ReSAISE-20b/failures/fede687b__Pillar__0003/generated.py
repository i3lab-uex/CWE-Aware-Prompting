import json
import csv
from io import TextIOWrapper, StringIO
from typing import Any


# Whitelist of safe serialization formats
ALLOWED_FORMATS = {"json", "csv"}


def deserialize_object(raw_data: bytes, format_type: str) -> Any:
    """
    Deserialize raw byte data into a Python object using the specified format.

    Parameters
    ----------
    raw_data : bytes
        The serialized data stream.
    format_type : str
        Serialization format. Supported values are 'json' and 'csv'.

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format_type is not supported or if deserialization fails.
    """
    # Validate the requested format
    if format_type not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization method: {format_type}")

    # Decode bytes to string for text-based formats
    try:
        data_str = raw_data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF-8") from exc

    if format_type == "json":
        try:
            return json.loads(data_str)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if format_type == "csv":
        # CSV is interpreted as a list of dictionaries (first row as header)
        try:
            csv_reader = csv.DictReader(StringIO(data_str))
            return [row for row in csv_reader]
        except Exception as exc:
            raise ValueError("Invalid CSV data") from exc