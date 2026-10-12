import json
import csv
from io import StringIO
from typing import Any, List, Dict

# Allowed serialization formats – only safe ones are permitted.
ALLOWED_METHODS = {"json", "csv"}


def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize `stream_bytes` according to the specified `method_type`.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        Serialization format used. Must be one of the allowed methods.

    Returns
    -------
    Any
        The deserialized Python object. For JSON it will be a dict/list,
        for CSV it will be a list of dictionaries.

    Raises
    ------
    ValueError
        If `method_type` is not supported or considered insecure.
    """
    method = method_type.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type}")

    # Convert bytes to string assuming UTF-8 encoding
    try:
        text = stream_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input bytes could not be decoded as UTF-8") from exc

    if method == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # CSV is read into a list of dictionaries (one per row)
        csv_reader = csv.DictReader(StringIO(text))
        return [row for row in csv_reader]

    # This point should never be reached because of the allowed methods check
    raise ValueError(f"Unhandled method: {method_type}")