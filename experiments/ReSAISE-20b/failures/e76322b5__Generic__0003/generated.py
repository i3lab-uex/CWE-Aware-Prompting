import json
import csv
from io import BytesIO
from typing import Any, List, Dict

# Define the set of accepted serialization formats.
ALLOWED_FORMATS = {"json", "csv"}

def decode_data(encoded_bytes: bytes, format_name: str) -> Any:
    """
    Deserialize `encoded_bytes` according to the specified serialization format.

    Parameters
    ----------
    encoded_bytes : bytes
        The serialized input stream.
    format_name : str
        The name of the serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it can be any valid JSON type.
        For CSV it returns a list of dictionaries where keys are column names.

    Raises
    ------
    ValueError
        If `format_name` is not in the list of allowed formats or if an insecure
        serialization method such as pickle is requested.
    """
    fmt = format_name.lower()
    if fmt not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported or insecure serialization format: {format_name}")

    if fmt == "json":
        # JSON is safe for deserialization as it only creates basic Python types.
        return json.loads(encoded_bytes.decode("utf-8"))

    if fmt == "csv":
        # CSV is parsed into a list of dictionaries (rows).
        with BytesIO(encoded_bytes) as bio:
            reader = csv.DictReader(io.TextIOWrapper(bio, encoding="utf-8"))
            return [row for row in reader]

    # The code should never reach here because of the allowed formats check.
    raise ValueError(f"Unhandled format: {format_name}")