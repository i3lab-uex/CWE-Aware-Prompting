import json
import csv
import io
from typing import Any, List, Dict

# Allowed serialization formats.  Pickle is explicitly excluded because it can
# execute arbitrary code during unpickling and is therefore considered unsafe.
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize the given byte stream according to the specified serialization
    format.

    Parameters
    ----------
    stream_bytes : bytes
        The raw input data to deserialize.
    method_type : str
        One of the supported serialization formats: 'json' or 'csv'.

    Returns
    -------
    Any
        The Python object obtained from deserialization.  For CSV the function
        returns a list of dictionaries, each representing one row.

    Raises
    ------
    ValueError
        If an unsupported or insecure serialization method is requested.
    """
    if method_type not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization format: {method_type}")

    # Common conversion from bytes to text
    try:
        text = stream_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Input data is not valid UTF‑8") from exc

    if method_type == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON data") from exc

    if method_type == "csv":
        # Use StringIO to treat the string as a file-like object for csv
        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # This point should never be reached due to the earlier check
    raise ValueError(f"Unhandled serialization method: {method_type}")