import json
import csv
from io import BytesIO, TextIOWrapper
from typing import Any, List, Dict

# Define the set of serialization methods that are considered safe.
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object using the specified method.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format used. Must be one of the allowed methods.

    Returns
    -------
    Any
        The deserialized Python object. For JSON, a native Python structure.
        For CSV, a list of dictionaries representing rows.

    Raises
    ------
    ValueError
        If the specified method is not in the set of allowed methods.
    """
    method = method_type.lower()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: {method_type}")

    if method == "json":
        # json.loads expects a str; decode using utf-8
        return json.loads(stream_bytes.decode("utf-8"))

    if method == "csv":
        # Use TextIOWrapper to convert bytes to text for csv reader
        with BytesIO(stream_bytes) as bio:
            with TextIOWrapper(bio, encoding="utf-8") as text_stream:
                reader = csv.DictReader(text_stream)
                # Convert each row to a dict and collect into a list
                return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled method: {method_type}")