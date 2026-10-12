import json
import csv
from io import StringIO, BytesIO
from typing import Any

# Define the set of allowed serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` according to the specified serialization format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        Name of the serialization format (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the format is unsupported, insecure, or if deserialization fails.
    """
    # Normalise format name to lower case
    fmt = format_name.lower()

    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: '{format_name}'")

    try:
        if fmt == "json":
            # json.loads expects a str; decode bytes safely
            return json.loads(encoded_bytes.decode("utf-8"))

        elif fmt == "csv":
            # CSV is parsed into a list of dictionaries
            with StringIO(encoded_bytes.decode("utf-8")) as csv_file:
                reader = csv.DictReader(csv_file)
                return [row for row in reader]

        else:
            # This branch is unreachable because of the earlier check,
            # but kept for completeness.
            raise ValueError(f"Unhandled format: {format_name}")

    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Failed to decode {format_name} data: {exc}") from exc
    except csv.Error as exc:
        raise ValueError(f"Failed to parse CSV data: {exc}") from exc