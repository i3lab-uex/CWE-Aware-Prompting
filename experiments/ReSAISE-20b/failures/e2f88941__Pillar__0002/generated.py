import json
import csv
from io import StringIO, BytesIO

def convert_bytes(data_bytes: bytes, format_method: str):
    """
    Deserialize a byte stream into a Python object using only approved methods.

    Parameters
    ----------
    data_bytes : bytes
        Serialized data.
    format_method : str
        Serialization method identifier (e.g., 'json', 'csv').

    Returns
    -------
    object
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested format is not supported or disallowed.
    """
    # List of safe, approved deserialization methods
    SAFE_METHODS = {"json", "csv"}

    fmt = format_method.lower()
    if fmt not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed or unrecognized.")

    if fmt == "json":
        # JSON expects a text string; decode using UTF-8
        try:
            decoded = data_bytes.decode("utf-8")
            return json.loads(decoded)
        except UnicodeDecodeError as e:
            raise ValueError("Data could not be decoded as UTF-8 for JSON.") from e
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON data.") from e

    if fmt == "csv":
        # CSV is read as text; decode using UTF-8
        try:
            decoded = data_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError("Data could not be decoded as UTF-8 for CSV.") from e

        # Use StringIO to provide a file-like object to csv.DictReader
        f = StringIO(decoded)
        reader = csv.DictReader(f)
        return [row for row in reader]

    # This point should never be reached due to the SAFE_METHODS check
    raise ValueError(f"Unhandled format method: {format_method}")