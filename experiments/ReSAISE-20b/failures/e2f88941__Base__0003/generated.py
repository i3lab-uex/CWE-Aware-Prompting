import json
import csv
from io import StringIO
from typing import Any, Dict, List


# Only these serialization methods are considered safe.
SAFE_METHODS = {"json", "csv"}


def convert_bytes(data_bytes: bytes, format_method: str) -> Any:
    """
    Deserialize a byte stream into its corresponding Python object using only
    whitelisted serialization methods.

    Parameters
    ----------
    data_bytes : bytes
        The serialized data to be deserialized.
    format_method : str
        Identifier of the serialization method used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object.

    Raises
    ------
    ValueError
        If the requested serialization method is not in SAFE_METHODS or is
        unrecognized.
    """
    if format_method.lower() not in SAFE_METHODS:
        raise ValueError(f"Deserialization method '{format_method}' is not allowed.")

    if format_method.lower() == "json":
        # json.loads can handle bytes directly, but decoding to str ensures
        # consistent behavior across Python versions.
        text = data_bytes.decode("utf-8")
        return json.loads(text)

    if format_method.lower() == "csv":
        # Interpret the bytes as UTF‑8 encoded CSV data.
        text = data_bytes.decode("utf-8")
        reader = csv.DictReader(StringIO(text))
        return [row for row in reader]

    # This point should never be reached because of the SAFE_METHODS check,
    # but we keep it for defensive programming.
    raise ValueError(f"Unsupported deserialization method: {format_method}")