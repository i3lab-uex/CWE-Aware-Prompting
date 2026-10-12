import json
import csv
import io
from typing import Any, List, Dict

# Define the set of serialization methods that are considered safe
ALLOWED_METHODS = {"json", "csv"}

def parse_stream(stream_bytes: bytes, method_type: str) -> Any:
    """
    Deserialize a byte stream into a Python object based on the specified method.

    Parameters
    ----------
    stream_bytes : bytes
        The serialized input data.
    method_type : str
        The serialization format used (e.g., 'json', 'csv').

    Returns
    -------
    Any
        The deserialized Python object. For JSON it will be a dict/list.
        For CSV it will be a list of dictionaries (one per row).

    Raises
    ------
    ValueError
        If the requested method_type is not in ALLOWED_METHODS.
    """
    # Normalise the method name
    method = method_type.lower()

    if method not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported or insecure serialization method: '{method_type}'")

    if method == "json":
        # JSON expects a text stream; decode from UTF-8
        try:
            return json.loads(stream_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid JSON data") from exc

    if method == "csv":
        # CSV is read as text; decode to UTF-8
        try:
            text = stream_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("CSV data is not valid UTF-8") from exc

        reader = csv.DictReader(io.StringIO(text))
        return [row for row in reader]

    # The code should never reach here because all allowed methods are handled above
    raise ValueError(f"Unhandled method type: {method_type}")