import json
import csv
from io import StringIO, BytesIO
from typing import Any


# List of serialization formats that are considered safe for this application.
TRUSTED_FORMATS = {"json", "csv"}


def load_object(serialized_data: bytes, deserialization_method: str) -> Any:
    """
    Deserialize a Python object from a byte stream using a specified method.

    Parameters
    ----------
    serialized_data : bytes
        The raw byte stream containing the serialized data.
    deserialization_method : str
        The name of the serialization format to use (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON, this will be a standard
        Python data structure (dict/list/etc.). For CSV, a list of dictionaries,
        where each dictionary represents one row with column names as keys.

    Raises
    ------
    ValueError
        If the requested deserialization method is not in the list of trusted
        formats or if an error occurs during parsing.
    """
    method = deserialization_method.lower()

    if method not in TRUSTED_FORMATS:
        raise ValueError(f"Unsupported or unsafe deserialization method: {method}")

    try:
        if method == "json":
            # json.loads expects a string; decode using UTF-8.
            text = serialized_data.decode("utf-8")
            return json.loads(text)

        if method == "csv":
            # csv module works with text streams. Convert bytes to a StringIO.
            text_stream = StringIO(serialized_data.decode("utf-8"))
            reader = csv.DictReader(text_stream)
            # Return a list of dictionaries, one per row.
            return [row for row in reader]

    except Exception as exc:
        # Wrap any exception to avoid leaking internal details.
        raise ValueError(f"Failed to deserialize data using {method}: {exc}") from exc