import json
import csv
from io import StringIO
from typing import Any


# List of serialization methods that are considered safe for deserialization.
SAFE_METHODS = {"json", "csv"}


def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    pre-approved serialization methods.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data.
    format_method : str
        Identifier of the serialization method used ('json' or 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON this can be any JSON-compatible
        type; for CSV it returns a list of dictionaries where keys are column
        headers.

    Raises
    ------
    ValueError
        If `format_method` is not in the list of allowed methods.
    """
    if format_method.lower() not in SAFE_METHODS:
        raise ValueError(
            f"Deserialization method '{format_method}' is not allowed or "
            "unrecognized. Allowed methods: 'json', 'csv'."
        )

    # Decode bytes to string using UTF-8 (common for text-based formats).
    try:
        data_str = data_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Data bytes are not valid UTF-8.") from exc

    if format_method.lower() == "json":
        # json.loads safely parses JSON into Python objects.
        return json.loads(data_str)

    if format_method.lower() == "csv":
        # Use csv.DictReader to read CSV data into a list of dicts.
        f = StringIO(data_str)
        reader = csv.DictReader(f)
        return [row for row in reader]